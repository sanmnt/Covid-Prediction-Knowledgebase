import mysql.connector

mydb = mysql.connector.connect(
    host="172.17.0.2",
    user="root",
    password="tPzk62XiHk6tXV",
    database="Covid_database"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT COUNT(*) FROM user_data WHERE prediction > 0.75 AND age < 0.35;")

myresult = mycursor.fetchall()

for x in myresult:
    print(x)
