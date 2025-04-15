import mysql.connector

# Establish connection to MySQL
connection = mysql.connector.connect(
    host="localhost", 
    user="root", 
    password="", 
    database="online_course"
)

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"  # You can change this to a secure password

# Function to login as admin
def login():
    print("Admin Login")
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("\n✅ Login successful!")
        return True
    else:
        print("\n❌ Invalid username or password. Access denied.")
        return False

# Function to show courses in the Courses table
def show_courses():
    cursor = connection.cursor()
    cursor.execute("SELECT course_id, title FROM Courses")
    courses = cursor.fetchall()
    
    print("\nAvailable Courses:")
    for course in courses:
        print(f"{course[0]} - {course[1]}")
    
    cursor.close()
    return courses

# Function to update course details
def update_course(course_id):
    cursor = connection.cursor()

    # Get the current course details
    cursor.execute("SELECT title, description, instructor FROM Courses WHERE course_id = %s", (course_id,))
    course = cursor.fetchone()

    if course:
        print(f"\nCurrent details of the course '{course[0]}':")
        print(f"Title: {course[0]}")
        print(f"Description: {course[1]}")
        print(f"Instructor: {course[2]}")
        
        # Prompt the user to enter new details
        new_title = input(f"Enter new title (or press Enter to keep '{course[0]}'): ") or course[0]
        new_description = input(f"Enter new description (or press Enter to keep '{course[1]}'): ") or course[1]
        new_instructor = input(f"Enter new instructor name (or press Enter to keep '{course[2]}'): ") or course[2]
        
        # Update the course with the new details
        cursor.execute("""
            UPDATE Courses
            SET title = %s, description = %s, instructor = %s
            WHERE course_id = %s
        """, (new_title, new_description, new_instructor, course_id))

        connection.commit()  # Commit the changes
        print(f"\n✅ Course ID {course_id} updated successfully!")
    else:
        print(f"\n❌ Course ID {course_id} not found.")
    
    cursor.close()

# Function to add a new course
def add_course():
    cursor = connection.cursor()

    title = input("Enter course title: ")
    description = input("Enter course description: ")
    instructor = input("Enter instructor name: ")

    # Insert new course into the 'Courses' table
    cursor.execute("INSERT INTO Courses (title, description, instructor) VALUES (%s, %s, %s)",
                   (title, description, instructor))

    connection.commit()  # Commit the transaction
    print(f"\n✅ Course '{title}' added successfully!")

    cursor.close()

# Function to view all data from a table
def view_table_data():
    table_name = input("\nEnter table name to view (e.g., 'Courses', 'Users', 'Enrollments' ,'Progress'): ")
    
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    print(f"\nData from '{table_name}' table:")
    for row in rows:
        print(row)

    cursor.close()

# Admin Menu for performing actions
def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. View Table Data")
        print("2. Add a New Course")
        print("3. Update an Existing Course")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ")

        if choice == "1":
            view_table_data()
        elif choice == "2":
            add_course()
        elif choice == "3":
            courses = show_courses()  # List courses first
            try:
                course_choice = int(input("\nEnter the course ID to update (or 0 to exit): "))
                if course_choice == 0:
                    print("Exiting...")
                    continue
                elif any(course[0] == course_choice for course in courses):
                    update_course(course_choice)
                else:
                    print("❌ Invalid course ID.")
            except ValueError:
                print("❌ Invalid input. Please enter a valid course ID.")
        elif choice == "4":
            print("\nGoodbye!")
            break
        else:
            print("❌ Invalid choice. Please select between 1-4.")

# Main Function
def main():
    if login():
        admin_menu()

    # Close the connection when done
    connection.close()

if __name__ == "__main__":
    main()
