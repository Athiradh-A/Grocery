#Libraries required for program 
import inquirer
from colored import fg,bg,attr
from texttable import *
import mysql.connector as db

#Connection with MySQL Database
connection = db.connect(host = 'localhost',
                      user = 'root', passwd = 'admin')
print(fg(200)+"You're now conencted to MySQL"+attr(0))

cursor = connection.cursor()
cursor.execute("use Grocery")

passw = "9215627"

passwd = input("Password : ")



if passwd == passw:
    print(fg(200) + "You're the admin"+ attr(0))
    #Program to ask user for their choice
    more = 'Y'
    while more.lower() == 'y':
        Query = [
        inquirer.List("Inventory",
                    message = "select option",
                    choices = ["All Records","Select record","Add Record"])
        ]

        Queryans = inquirer.prompt(Query)
        #Program to show all records in a proper table manner 
        if Queryans["Inventory"] == 'All Records':
            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.set_cols_dtype(['t','t','i','i',])
            table.set_cols_align(["m","m","m","m",])
            tableList = [["Item Code","Item Name","Qty","Price"]]
            cursor.execute("select * from Items")
            records = cursor.fetchall()
            for row in records:
                tableList.append(
                        [row[0],row[1],row[2],row[3]])
            table.add_rows(tableList)
            print(table.draw())

        #Program to show any one record
        elif Queryans["Inventory"] == 'Select record':
            code = str(input(fg(200) + "Enter Item code : "+ attr(0)))
            cursor.execute("select * from Items "+"where Item_code ='%s'"%(code)+";")
            record = cursor.fetchall()
            for row in record:
                print("Item code :",fg(23) +str(row[0]) + attr(0))
                print("Item Name :",fg(23) +str(row[1]) + attr(0))
                print("Qantity Left :",fg(23) +str(row[2]) + attr(0))
                print("Price :",fg(23) +str(row[3]) + attr(0))

        #Program to add new record of item into the table 
        elif Queryans["Inventory"] == 'Add Record':
            itcode = input(fg(197) + "Enter Item code :"+ attr(0))
            itname = input(fg(197) + "Enter item name :"+ attr(0))
            quan = int(input(fg(197) + "Quantity in stock :"+ attr(0)))
            price = int(input(fg(197) + "price :"+ attr(0)))
            ins = "insert into Items values(%s,%s,%s,%s)"
            dat = (itcode,itname,quan,price)
            cursor.execute(ins,dat)
            print(fg(33) + "Added Data"+ attr(0))
            connection.commit()
        
        more = input(fg(22) + "Want to do more?(Y/N) :"+ attr(0))
#If passwd wrong, to show you're not admin
else:
            print(fg(27) + "You're not the admin" + attr(0))       
