# libraries required
import mysql.connector as db
from texttable import Texttable

def show_items():
    connection = db.connect(host='localhost', user='root', passwd='admin', database="Grocery")
    cursor = connection.cursor()
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype(['t', 'i'])
    table.set_cols_align(["m", "m"])
    tableList = [["Item Name", "Price"]]
    cursor.execute("SELECT Item_name, Price FROM Items")
    for row in cursor.fetchall():
        tableList.append([row[0], row[1]])
    table.add_rows(tableList)
    print(table.draw())
    connection.close()
