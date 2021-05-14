import mysql.connector

mydb = mysql.connector.connect(
    host="172.17.0.2",
    user="root",
    password="tPzk62XiHk6tXV",
    database="Covid_database"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT (SELECT COUNT(*) FROM user_data WHERE prediction > 0.75 AND smoker = 'True') / COUNT(*) AS 'Percentage' FROM user_data;")

myresult = mycursor.fetchall()

for x in myresult:
    print(x)
