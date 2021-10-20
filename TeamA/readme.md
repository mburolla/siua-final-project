# SIUA: Final Project
#This is where we are documenting our solution, if a new member came to the team this is how they would get up to speed.




#UIM (User Input Module)
This py is to take input and then push that input to the AWS DB. We are using MysqlWorkbench as our databse GUI.
    def createConnection(): This is where we make the connected to the database
    def customerId(): This is where we take the customer's id and validate it
    def username(): This is where we take the username and validate it
    def quantity(): This is to take the quantity input and validate it
    def insertCustomerData(customer_id, username,quantity): This function is how we format and push our data to the DB
    def main(): where we create the loop for inputs to run continously 



#BEM (Billing Engine Module)
Our program starts with UIM (User input module) allowing the user to input a customer id, username, and quantity number

from there that information will be stored in a database

BEM (billing engine module) pulls the stored data from said database, sorts the data, modifies certain data, and sends new modified data in a .txt file to Amazon S3 where the file can be viewed.


