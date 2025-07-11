from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
import random

# Set base directory and consistent DB path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

app = Flask(__name__)
app.secret_key = "Abdulsobur#Muhammad"  # For session security

# Create the students table if it doesn't exist
def student_init_db():
    print(f"✅ Creating DB at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lastname TEXT NOT NULL,
            firstname TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            dob TEXT NOT NULL,
            gender TEXT NOT NULL,
            currentClass TEXT NOT NULL,
            password TEXT NOT NULL,
            verified INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# Student registration route
@app.route("/register_student", methods=["GET", "POST"])
def register_student():
    if request.method == "POST":
        # Get form data
        lastname = request.form.get("Lastname")
        firstname = request.form.get("Firstname")
        username = request.form.get("Username")
        email = request.form.get("email")
        dob = request.form.get("DOB")
        gender = request.form.get("gender")
        student_class = request.form.get("class")
        password = request.form.get("initialPassword")
        confirm_password = request.form.get("finalPassword")

        print("📥 Form received:", lastname, firstname, username, email)

        # Backend password match check
        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("register_student"))

        # Insert into database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO students (
                    lastname, firstname, username, email, dob, gender, currentClass, password, verified
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
            """, (lastname, firstname, username, email, dob, gender, student_class, password))
            conn.commit()
        except sqlite3.IntegrityError as e:
            print("❌ DB insert failed:", e)
            flash("Username or Email already exists.")
            return redirect(url_for("register_student"))
        finally:
            conn.close()

        # Generate 6-digit verification code
        code = str(random.randint(100000, 999999))
        session["verification_code"] = code
        session["student_email"] = email
        print(f"📧 Verification code for {email}: {code}")

        return redirect(url_for("verify_email"))

    return render_template("register/register_student.html")

# Dummy email verification page
@app.route("/verify-email", methods=["GET", "POST"])
def verify_email():
    return render_template("register/verify_email.html")

# Run the Flask app
if __name__ == "__main__":
    student_init_db()
    app.run(debug=True)