# main.py

from course_app import connection
import random

# ===== Login Function =====
def login_user():
    cursor = connection.cursor()

    email = input("📧 Enter your email: ")
    password = input("🔒 Enter your password: ")

    cursor.execute("SELECT user_id, name FROM Users WHERE email = %s AND password = %s AND role = 'student'", (email, password))
    user = cursor.fetchone()

    if user:
        print(f"\n✅ Welcome, {user[1]}!")
        return user[0], user[1]  # return user_id, name
    else:
        print("\n❌ Invalid login credentials.")
        return None, None

# ===== Show Courses =====
def show_courses():
    cursor = connection.cursor()
    cursor.execute("SELECT course_id, title FROM Courses")
    courses = cursor.fetchall()

    print("\n📚 Available Courses:")
    for course in courses:
        print(f"{course[0]} - {course[1]}")

    cursor.close()
    return courses

# ===== Enroll Student and Generate Progress =====
def enroll_student(user_id, course_id):
    cursor = connection.cursor()

    # Check if already enrolled
    cursor.execute("SELECT * FROM Enrollments WHERE user_id = %s AND course_id = %s", (user_id, course_id))
    already_enrolled = cursor.fetchone()

    if already_enrolled:
        print("\n⚠️ You're already enrolled in this course.")
    else:
        cursor.execute("INSERT INTO Enrollments (user_id, course_id) VALUES (%s, %s)", (user_id, course_id))

        # Get enrollment_id
        cursor.execute("SELECT enrollment_id FROM Enrollments WHERE user_id = %s AND course_id = %s", (user_id, course_id))
        enrollment_id = cursor.fetchone()[0]

        progress = random.randint(10, 100)
        cursor.execute("INSERT INTO Progress (enrollment_id, completed_pct) VALUES (%s, %s)",
                       (enrollment_id, progress))

        connection.commit()
        print(f"\n✅ Enrolled successfully! Initial Progress: {progress}%")

    cursor.close()

# ===== Show Progress =====
def show_progress(user_id):
    cursor = connection.cursor()

    query = """
    SELECT c.title, p.completed_pct
    FROM Progress p
    JOIN Enrollments e ON p.enrollment_id = e.enrollment_id
    JOIN Courses c ON e.course_id = c.course_id
    WHERE e.user_id = %s
    """
    cursor.execute(query, (user_id,))
    results = cursor.fetchall()

    print("\n📈 Your Progress:")
    for row in results:
        print(f"📘 {row[0]}: {row[1]}%")

    cursor.close()

# ===== MAIN APP FLOW =====
def main():
    print("==== Student Login ====")
    user_id, user_name = login_user()

    if not user_id:
        return

    while True:
        # Show available courses
        courses = show_courses()

        try:
            course_id = int(input("\n👉 Enter course ID to enroll (or 0 to exit): "))
            if course_id == 0:
                print("Goodbye!")
                break
        except ValueError:
            print("❌ Invalid course ID.")
            continue

        # Enroll the user in the selected course
        enroll_student(user_id, course_id)

        # Offer user to either view progress or enroll in another course
        while True:
            choice = input("\nChoose an option:\n1. View Progress\n2. Enroll in Another Course\n3. Exit\n> ")

            if choice == '1':
                show_progress(user_id)
            elif choice == '2':
                break  # Exit inner loop and show courses again
            elif choice == '3':
                print("Goodbye!")
                return
            else:
                print("❌ Invalid choice. Please select again.")

    connection.close()

if __name__ == "__main__":
    main()
