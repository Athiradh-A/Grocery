import mysql.connector as db
from texttable import Texttable
from colored import fg, attr
import random
from datetime import datetime

def start_checkout():
    connection = db.connect(host='localhost', user='root', passwd='admin', database="Grocery")
    cursor = connection.cursor()
    bill = "Y"
    tableList = []
    bill_amt = 0

    bought_items = []

    while bill.lower() == 'y':
        item = str(input(fg(21) + "Name of item :" + attr(0)))
        Quan = int(input(fg(21) + "Quantity of item :" + attr(0)))
        cursor.execute("SELECT Price, Qty FROM Items WHERE Item_name=%s", (item,))
        res = cursor.fetchone()

        if not res or res[1] < Quan:
            print(fg(160) + 'Item not available or not enough quantity!!' + attr(0))
        else:
            price = res * Quan
            bill_amt += price
            bought_items.append((item, Quan, res, price))
            cursor.execute("UPDATE Items SET Qty=Qty-%s WHERE Item_name=%s", (Quan, item))
            connection.commit()
        bill = input(fg(21) + "Add more items? (Y/N):" + attr(0))

    # Supermarket-style bill
    if bought_items:
        print("\n" + "="*36)
        print("       FRESH GROCERY SUPERMARKET      ")
        print("="*36)
        bill_no = random.randint(100000, 999999)
        now = datetime.now()
        print(f"Bill No : {bill_no}")
        print(f"Date    : {now.strftime('%d-%m-%Y')}")
        print(f"Time    : {now.strftime('%I:%M %p')}")
        print("-"*36)
        print(f"{'Item':<15}{'Qty':<6}{'Rate':<7}{'Amt':>7}")
        print("-"*36)
        for itm, qty, rate, amt in bought_items:
            print(f"{itm:<15}{qty:<6}{rate:<7}{amt:>7}")
        print("-"*36)
        print(f"{'TOTAL':<28}{bill_amt:>7}")
        print("="*36)
        print("   Thank you for shopping with us!   ")
        print("="*36 + "\n")
    else:
        print("No items purchased.")

    connection.close()
