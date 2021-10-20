# SIUA: Final Project
#This is where we are documenting our solution, if a new member came to the team this is how they would get up to speed.
There are 4 parts to this project UIM > Aurora DB > BEM > S3. Below will explain each part of the project. 



#UIM (User Input Module)
This py is to take input and then push that input to the AWS DB. We are using MysqlWorkbench as our databse GUI.
    The UIM is written in Python and accepts user input from the console. 
    The input consists of a customer id, username, and quantity. For example:
        The customer id does not contain leading zeros. The customer name only contains a first andlast name. 
        The quantity is a positive integer greater than zero, less than 1,000.
        The UIM stores the customer id, username, and quantity in a database table. 
    The program runsindefinitely until control+c is entered on the console.  


#Aurora DB
The database stores all the data entered from the UIM. Each SIUA group has their own DB
schema (fp-group{group number}). The database is secured using an AWS security group and
is only accessible only to SIUA students.


#BEM (Billing Engine Module)
BEM (billing engine module) pulls the stored data from said database, sorts the data, modifies certain data, and sends new modified data in a .txt file to Amazon S3 where the file can be viewed.
    The BEM is written in Python and calculates the amount to bill a customer. 
        The billing rates for the biling engine are as follows:
            1-10 Quantity = $5 dollar billable amount
            11-20 Quantity = $4 dollar billable amount
            >20 Quantity = $3 dollar billable amount
    When the dollar amounts for all the customers have been calculated, the BEM saves this information to a textfile located in S3. 
    Customers are aggregated by username preventing duplicate usernames in the final output file. 
The BEM runs every 60 seconds until control+c is entered on the console.


#S3
Amazon’s Simple Storage Solution stores text files for all the customers to be billed in a bucket named siua-billable-customers. 
Text files are stored in this bucket with the following key path schema:
    {group number}/billable_customers.txt
The S3 file must be formatted in a specific way. Details listed below:
    Customer ID = 10 digits long, left padded with zeros
    Name = The name of the customer
    Quantity = Number
    Total Amount = US dollar amount


Non-Functional Requirements
All Python code is submitted to the GitHub repository: siua-final-project with one final Pull Request (PRs) for the instructor to review and merge into the working branch.
Python code does not “leak” database connections. The AWS database connection graph is used to monitor database connections.


Stretch Goals
[BEM]Use Forever to run the BEM as a Forever process on your computer.
[S3]Store the customer IDs in the text file in ascending order
[Python]Store the customer IDs in the text file in ascending order
[UIM] Implement the following validation rules for the UIM. If one or more validation rules fail an appropriate error message is displayed on the console:
    ● Customer id must be a valid number
    ● Name must only contain letters
    ● Quantity must be a valids number
    ● All three fields must be required
    ● A comma must be used to separate fields
