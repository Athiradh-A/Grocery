# emp.py
import mysql.connector as db
from texttable import Texttable
import inquirer

def manage_employees():
    connection = db.connect(host='localhost', user='root', passwd='admin', database="Grocery")
    cursor = connection.cursor()

    query = [
        inquirer.List("action",
                      message="Select option:",
                      choices=["Show all records", "Get specific record", "Add Record"])
    ]
    res = inquirer.prompt(query)

    if res["action"] == "Show all records":
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(['t','t','i','i','t'])
        table.set_cols_align(["m","m","m","m","m"])
        tableList = [["Employee Id","Name","Age","Salary","Phone"]]
        cursor.execute("SELECT * FROM Employee")
        for row in cursor.fetchall():
            tableList.append([row[0], row[1], row[2], row[3], row[4]])
        table.add_rows(tableList)
        print(table.draw())

    elif res["action"] == "Get specific record":
        empid = input("Enter employee id: ")
        cursor.execute("SELECT * FROM Employee WHERE Empid=%s", (empid,))
        for row in cursor.fetchall():
            print("Employee id:", row[0])
            print("Name:", row[1])
            print("Age:", row[2])
            print("Salary:", row[3])
            print("Phone:", row[4])

    elif res["action"] == "Add Record":
        eid = input("Employee id: ")
        name = input("Name: ")
        age = input("Age: ")
        sal = input("Salary: ")
        phone = input("Phone number: ")
        cursor.execute("INSERT INTO Employee VALUES (%s,%s,%s,%s,%s)", (eid, name, age, sal, phone))
        connection.commit()
        print("Added successfully")

    connection.close()
