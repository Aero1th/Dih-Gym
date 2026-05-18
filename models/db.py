import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='gym_management_system'
)

cursor = connection.cursor(dictionary=True)