#Libraries required for program 
from texttable import * 
import mysql.connector as db


#Connection with MySQL Database
connection = db.connect(host = 'localhost',
                      user = 'root', passwd = 'admin')

#Program to show list of all items and their prices in a proper table manner
cursor = connection.cursor()
cursor.execute("use Grocery")
table = Texttable()
table.set_deco(Texttable.HEADER)
table.set_cols_dtype(['t','i',])
table.set_cols_align(["m","m",])
tableList = [["Item Name","Price"]]
cursor.execute("select Item_name,Price from Items")
records = cursor.fetchall()
for row in records:
        tableList.append(
                [row[0],row[1]])
table.add_rows(tableList)
print(table.draw())