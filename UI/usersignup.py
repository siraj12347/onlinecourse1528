import mysql.connector

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="online_course"
)

# Function to register a new student
def register_student(name, email, password):
    cursor = connection.cursor()

    # Check if email already exists
    cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        print("\n❌ This email is already registered. Try logging in.")
    else:
        role = "student"
        query = "INSERT INTO Users (name, email, password, role) VALUES (%s, %s, %s, %s)"
        values = (name, email, password, role)
        cursor.execute(query, values)
        connection.commit()
        print(f"\n✅ Student '{name}' registered successfully!")

    cursor.close()

# ===== Get user input =====
name = input("Enter your name: ")
email = input("Enter your email: ")
password = input("Create a password: ")

register_student(name, email, password)

# Close the connection
connection.close()
