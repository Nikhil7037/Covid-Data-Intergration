import mysql.connector
import matplotlib as plt
import plotly.express as plot

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

    #for x in result:
        #print(x);

    cur.execute("select Date from covid where country='china'")
    result1=cur.fetchall()




    for x in result1:
        print(x);

    fig = plot.bar(result1, 'china')
    fig.show()



except:
    myconn.rollback()

myconn.close()