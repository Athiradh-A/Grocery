#Libraries required for project 
from colored import fg,attr
import inquirer 
from texttable import *

print(fg(87) + "Welcome to Fresh Groces!!" + attr(0))

times = "y"
while times.lower() == 'y':
    #Query to ask user ther required action
    Loginquery = [
        inquirer.List("login",
                    message = "Choose your section : ",
                    choices = ["Checkout", "Employee records", "Inventory",], default = "checkout"),
    ]

    rec = inquirer.prompt(Loginquery)
    #Program for checkout 
    if rec["login"] == 'Checkout':
        print("Selected Checkout" + fg(23),attr(0))
        print(fg(36) + "Items Available And Price" + attr(0))
        from components import checkouttable
        from components import checkoutmain
        


    elif rec["login"] == "Employee records":
        #Program to Show all employee records, add new records and select a single record
        from components import emp

                
    elif rec["login"] == 'Inventory':
        #Program to show all item records, add new record, select a single item record
        print("Selected Inventory" + fg(23),attr(0))
        from components import inventory

    #Asking user if He/She wants to repeat program 
    times = input(fg(86)+"Want to do anything?\nCheckout\nEmployee records\nInventory\n(Y/N):"+attr(0))


#Good-Bye message to the user
print(fg(42)+"Thank you for visiting!!\nHave a nice day!!"+attr(0))