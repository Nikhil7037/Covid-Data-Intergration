import json
import mysql.connector

myconn = mysql.connector.connect(host="localhost", user="root", passwd="Temp@123", database="test")

# creating the cursor object
cur = myconn.cursor()
fileObject = open("data.json", "r")
jsonContent = fileObject.read()
aList = json.loads(jsonContent)
print(aList)
print(aList['a'])
print(aList['b'])
print(aList['c'])
x=aList['a']
y=aList['b']
z=aList['c']


sql = "INSERT INTO covid (country, date,cases) VALUES (%s, %s,%s)"
val = (x,y,z)
cur.execute(sql, val)

myconn.commit()

print(cur.rowcount, "record inserted.")

