#Libraries required for the program
import mysql.connector as db
from colored import fg, bg, attr
from texttable import *
import inquirer

#Connection with MySQL Database
print("==================================================")
print("%s Initializing connection to mySQL server %s" % (fg(51), attr(0)))
connection=db.connect(host = 'localhost',
                      user = 'root', passwd = 'admin')
db_Info = connection.get_server_info()
print(fg(50)+" Connected to MySQL Server version " + db_Info + attr(0))
                
cursor = connection.cursor()
cursor.execute("use grocery")

passwd = 9215627
code = int(input(fg(23)+"Enter Passcode:"+attr(0)))

if code == passwd:
#Query to select options from User 
    QueryDef = [
        inquirer.List("read", message="Select option :",
                    choices=["Show all records", "Get specific record","Add Record"], default="Get specific record"),
    ]


    def main():
        print("%s Logged in as Admin %s" % (fg(51), attr(0)))

    def read():
        res = inquirer.prompt(QueryDef)
        #Program to show all records
        if (res['read'] == "Show all records"):
            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.set_cols_dtype(['t','t','i','i','t'])
            table.set_cols_align(["m","m","m","m","m"])
            tableList = [["Employee Id","Name","Age","Salary","Phone"]]
            cursor.execute("select * from Employee;")
            record = cursor.fetchall()
            for row in record:
                tableList.append(
                    [row[0], row[1], row[2], row[3], row[4]])
            table.add_rows(tableList)
            print(table.draw())

        #Program to show record of specified employee
        elif (res['read'] == "Get specific record"):
            color = fg(13)
            att = attr(0)
            admn = input(color + "Enter employee id  : " + att)
            print("==================================================")
            cursor.execute("select * from Employee "+"where Empid ="+admn+";")
            record = cursor.fetchall()
            for row in record:
                color = fg(50)
                att = attr(0)
                print("Employee id : "+color + str(row[0]) + att)
                print("Name: " + color + str(row[1]) + att)
                print("Age: " + color + str(row[2]) + att)
                print("Salary: " + color + str(row[3]) + att)
                print("Phone: "+ color + str(row[4]) + att)           
            print("==================================================")

        #Program to add new employee record
        elif (res['read'] == 'Add Record'):
            add = 'y'
            while add.lower() == 'y':
                color = fg(23)
                att=attr(0)
                eid = input('Employee id : ') 
                name = input('Name : ')  
                age = input('Age : ') 
                sal = input('Salary : ') 
                phone = input('Phone number : ') 
                commnd = "insert into Employee values(%s,%s,%s,%s,%s)"
                values = (eid,name,age,sal,phone)
                cursor.execute(commnd,values)
                connection.commit()
                print('===================================')
                print('Added' + color + att)
                add = input("Add more ? (Y?N) : ")


    main()
    read()

else:
    print(fg(169)+"You're not the admin!!"+attr(0))


