import pymysql
import boto3 
from time import sleep
from datetime import datetime
import numpy as np

INTERVAL_SECONDS = 60

def createConnection():
  '''Creates connection to AWS'''
  retval = None  
  USER = 'sia-db-user'
  HOST = 'sia-db-cluster-instance-1.cosgu9wr5iwp.us-east-1.rds.amazonaws.com'
  PWD = 'testtest'
  DB = 'TeamA'
  retval = pymysql.connect(
    user = USER,
    host = HOST,
    password = PWD,
    database = DB)
  return retval

def getQuantityData():
  '''Retrieves quantity data from customer_information table in MySQL Workbench'''
  retval = []
  conn = createConnection()
  with conn.cursor(pymysql.cursors.DictCursor) as cursor:
    cursor.execute('select sum(quantity) from customer_information group by username order by customer_id asc')    
    conn.commit()
    retval = cursor.fetchall()
  return retval

def getIdData():
  '''Retrieves id data from customer_information table in MySQL Workbench'''
  retval = []
  conn = createConnection()
  with conn.cursor(pymysql.cursors.DictCursor) as cursor:
    cursor.execute('select customer_id from customer_information group by username order by customer_id asc')
    conn.commit()
    retval = cursor.fetchall()
  return retval

def getUsernameData():
  '''Retrieves username data from customer_information table in MySQL Workbench'''
  retval = []
  conn = createConnection()
  with conn.cursor(pymysql.cursors.DictCursor) as cursor:
    cursor.execute('select username from customer_information group by username order by customer_id asc')
    conn.commit()
    retval = cursor.fetchall()
  return retval

def idData():
  '''Creates a list of ids from customer_information table'''
  id = getIdData()
  id_list = []
  for i in id:
      id = str(i['customer_id']).zfill(10)
      id_list.append(id)
  return(id_list)

def usernameData():
  '''Creates a list of usernames from customer_information table'''
  User = getUsernameData()
  username_list = []
  for u in User:
          user = u['username']
          username_list.append(user)
  return username_list

def quantityData():
  '''Creates a list of quantities from customer_information table'''
  quantity = getQuantityData()
  quantity_list = []
  for qu in quantity:
      quantity = qu['sum(quantity)']
      quantity_list.append(quantity)
  return quantity_list

def getValue():
  '''Creates a list of the multiplied quantity from customer_information table by corresponding amount'''
  data = getQuantityData()
  quantityList = []
  multiplied_list = []
  for qd in data:
      quantity = qd['sum(quantity)']
      quantityList.append(quantity)
  for q in quantityList:
      if q >= 1 and q <= 10:
          num = 5
      elif q >= 11 and q <= 20:
          num = 4
      elif q > 20:
          num = 3
      amount = q * num
      multiplied_list.append('${:,.2f}'.format(amount))
  return multiplied_list

def newCustomerList(multiplied_list, id_list, username_list, quantity_list):
  '''Creates new and updated lists with correct id, username, and multiplied quantity ready to push to S3'''
  new_list = []
  final_CL = []
  for i in range(0, len(id_list)):
      new_list.append(f"{id_list[i]}\t")
      new_list.append(f"{username_list[i]}\t")
      new_list.append(f"{quantity_list[i]}\t")
      new_list.append(f"{multiplied_list[i]}\t")
  newCL = np.array_split(new_list, len(id_list))
  for array in newCL:
      newCL = list(array)
      newCL = ' '.join([str(item) for item in newCL])
      final_CL.append(newCL)
  return final_CL

def createFileS3(list,fileHeader, bucketName, keyPath):
  '''Pushes data to S3'''
  retval = None
  client = boto3.client('s3')
  timeString = datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
  fileContents = f'{fileHeader}\nTime: {timeString}\n'
  for customerId in list:
    fileContents += f'{customerId}\n'
  retval = client.put_object(Body = fileContents, Bucket = bucketName, Key = keyPath)
  return retval

def main():
  while True:
    multiplied_list = getValue()
    id_list = idData()
    user_list = usernameData()
    quantity_list = quantityData()
    final_CL = newCustomerList(multiplied_list, id_list, user_list, quantity_list)
    billableCustomersList = final_CL
    createFileS3(list = billableCustomersList, fileHeader = '*** BILLABLE CUSTOMERS ***', bucketName = 'siua-billable-customers', keyPath ='TeamA/billable_customers.txt')
    
    timestamp = datetime.today().strftime('%m/%d/%Y %I:%M:%S %p')
    print(f'\nLast run: {timestamp}.\nThis is also running FOREVER. Check and kill our pid# for verification.')
    sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
  main()