# course_app.py
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="online_course"
)

if connection.is_connected():
    print('Connected Successfully')
else:
    print('Failed to connect')
