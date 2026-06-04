import os
import sys
import mysql.connector
from mysql.connector import Error

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
DB_NAME = os.environ.get('DB_NAME', 'gym_management_system')
DB_PORT = int(os.environ.get('DB_PORT', '3306'))

try:
    connection = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
except Error as err:
    print('ERROR: Could not connect to MySQL database.')
    print(f'  Host: {DB_HOST}:3306')
    print(f'  User: {DB_USER}')
    print(f'  Database: {DB_NAME}')
    print('Please start your MySQL server and verify the credentials.')
    print('If you are using XAMPP/WAMP/MAMP, make sure MySQL is running.')
    print('You can also set DB_HOST, DB_USER, DB_PASSWORD, and DB_NAME environment variables.')
    sys.exit(1)

cursor = connection.cursor(dictionary=True)