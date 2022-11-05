#Libraries required for project 
from colored import fg,attr
import inquirer 
from texttable import *


times = "y"
while times.lower() == 'y':
    #Query to ask user ther required action
    Loginquery = [
        inquirer.List("login",
                    message = "Choose your section : ",
                    choices = ["Checkout", "Employee records", "Inventory"], default = "checkout"),
    ]

    rec = inquirer.prompt(Loginquery)
    #Program for checkout 
    if rec["login"] == 'Checkout':
        print("Selected Checkout" + fg(23),attr(0))
        print(fg(36) + "Items Available And Price" + attr(0))
        from components import checkouttable
        from components import checkoutmain
        


    elif rec["login"] == "Employee records":
        time='y'
        #Program to Show all employee records, add new records and select a single record
        while time.lower() == 'y':
            from components import emp
            time = input('do more?(y/n) : ')
            if time.lower() == 'y':
                time = 'y'
            else:
                print(fg(200)+'End of search'+attr(0))

                
    elif rec["login"] == 'Inventory':
        #Program to show all records, add record, select a single record
        print("Selected Inventory" + fg(23),attr(0))
        from components import inventory

    #Asking user if He/She wants to repeat program 
    times = input(fg(86)+"Want to do anything?(Y/N):"+attr(0))


#Good-Bye message to the user
print(fg(42)+"Thank you for visiting!!\nHave a nice day!!"+attr(0))