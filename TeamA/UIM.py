import pymysql 

def createConnection():
  '''Connect to auroraDB'''
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


def customerId():
  '''takes input customerId'''
  retval = 0 
  keepGoing = True 
  while keepGoing: 
    userID = input('Id number: ') 
    usercheck = userID.isdigit() 
    if usercheck == False: 
      if (not userID): 
        print('you have to enter a number') 
        keepGoing = True 
      elif usercheck == False: 
        print('Only positive integers') 
        keepGoing = True 
    else:
      retval= int(userID) 
      keepGoing = False 
      return retval 
      
   
def username():
  '''take input username'''
  keepGoing = True 
  while keepGoing: 
    username = input('username: ') 
    checkusername = username.replace(" ", "") 
    bool = checkusername.isalpha() 
    firstlastcheck = username.split() 
    try: 
      if bool == False: 
        if (not username): 
          print('You need to actually enter a name') 
          keepGoing = True 
        elif bool == False: 
          print('Only Alpha characters') 
          keepGoing = True 
      elif firstlastcheck[-1] != firstlastcheck[1]: 
        print('First and last name please') 
        keepGoing = True 
      else:
          keepGoing = False
          return username 
    except IndexError  as i : 
      print(f'You did not type in a last named based on {i} error') 
      keepGoing = True 


def quantity():
  '''takes input quantity'''
  keepGoing = True 
  while keepGoing: 
    quantity = input('quantity: ').strip() 
    checkquantity = quantity.isdigit() 
    try: 
      retval = int(quantity)
      if checkquantity == False: 
        while retval <= 0: 
          if (retval <= 0 ): 
            print('Sorry that number is too low') 
            retval = int(input('quantity: ')) 
          else:
            keepGoing = True 
        while retval >= 1000: 
          if (retval >= 1000): 
            print('Sorry that number is too high') 
            retval = int(input('quantity: ')) 
        print('Enter a positive integer') 
        keepGoing = True
      else:
        keepGoing = False 
    except ValueError as v:
      print(f'Please enter a positive integer greater than zero and less than 1000.\nError: {v}. ') 
      keepGoing = True 
    if checkquantity == True: 
      while retval <= 0 or retval >= 1000: 
        if (retval <= 0 ): 
          print('Sorry that number is too low') 
          retval = int(input('quantity: ')) 
        elif (retval >= 1000): 
            print('Sorry that number is too high') 
            retval = int(input('quantity: ')) 
  return retval 


def insertCustomerData(customer_id, username,quantity):
  '''inserts data to auroraDB '''
  retval = 0
  conn = createConnection()
  with conn.cursor() as cursor: 
    cursor.execute("insert into customer_information (customer_id, username,quantity) values (%s, %s,%s)", (customer_id, username,quantity))
    retval = cursor.lastrowid 
    conn.commit() 
  return retval 

def main():
  while True: 
      customer_id_input = customerId() 
      username_input = username() 
      quantity_input = quantity() 
      insertCustomerData(customer_id_input, username_input, quantity_input)

if __name__ == "__main__":  
  main()