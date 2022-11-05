#Libraries required for this project 
import mysql.connector 
from colored import fg,attr,bg
import mysql.connector as db
from texttable import *


#Connection with MySQL Database
connection = db.connect(host = 'localhost',
                      user = 'root', passwd = 'admin')

cursor = connection.cursor()
cursor.execute("use Grocery")

#Program for checkout
bill = "Y"
tableList = [["Item name","Quantity","Price"]]
bill_amt = 0
while bill.lower() == 'y':
    #TO get input of Item name and Quantity user wants
    item = str(input(fg(21) + "Name of item :"+ attr(0)))
    Quan = int(input(fg(21) + "Quantity of item :"+ attr(0)))
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_cols_align(["m","m","m",])
    table.set_cols_dtype(["t","i","i",])
    cursor.execute("select Price from items"+" where Item_name='%s'"%(item))
    amt = cursor.fetchall()
    price = amt[0]*(Quan)
    bill_amt = bill_amt + sum(price)
    
    #Selecting from the Table Items
    cursor.execute("select Item_name,"+ str(Quan) +"*price from items"+" Where Item_name='%s'"%(item))
    items = cursor.fetchall()
    for zeroitem in items:
        if zeroitem[1] == 0:
            print(fg(160)+'Item not available!!'+attr(0))
            bill = input(fg(21)+"Add More?(Y/N): "+attr(0))
        else:
            #program to show to add more items 
            for thing in items:
                tableList.append(
                    [thing[0],Quan,sum(price)])
            table.add_rows(tableList)    
            bill = input(fg(21) + "Add more?(Y/N) : "+ attr(0))
            if bill.lower() == 'y':
                bill = 'Y'
            else :
                #Program to show Final bill in a proper table manner 
                print(fg(22)+table.draw()+attr(0))

            
            updat = "update items set Qty=Qty-%s"%(Quan)+" where Item_name='%s'"%(item)
            try:
                cursor.execute(updat)
                connection.commit()
                #closing connection with MySQL

            except:
                connection.rollback() 

print(fg(196)+"Your total is:"+str(bill_amt)+attr(0))
print(fg(200)+"Thanks for shopping with us!!"+attr(0))

    

