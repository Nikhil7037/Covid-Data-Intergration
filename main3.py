import mysql.connector

# Create the connection object
myconn = mysql.connector.connect(host="localhost", user="root", passwd="Temp@123", database="test")

# creating the cursor object
cur = myconn.cursor()

try:
    # Reading the Employee data
    cur.execute("select * from covid")

    # fetching the rows from the cursor object
    result = cur.fetchall()
    # printing the result

    for x in result:
        print(x);
except:
    myconn.rollback()

myconn.close()