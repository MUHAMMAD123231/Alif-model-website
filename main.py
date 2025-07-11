from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
import os
import random
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "Abdulsobur#Muhammad"

# --- Database Setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create Students table
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

    # Create Teachers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teacher (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            dob TEXT NOT NULL,
            gender TEXT NOT NULL,
            phoneNumber TEXT NOT NULL UNIQUE,
            subject TEXT NOT NULL,
            password TEXT NOT NULL,
            verified INTEGER DEFAULT 0
        )
    """)

    # Create Admin table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            dob TEXT NOT NULL,
            gender TEXT NOT NULL,
            phoneNumber TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL,
            password TEXT NOT NULL,
            verified INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

# --- Email Sender ---
def send_verification_email(to_email, code):
    sender_email = "akereleoluwanifemi26@gmail.com"
    sender_password = "dtjakyznezmxoesy"  # Gmail App Password

    body = f"Hello,\n\nYour verification code is: {code}\n\nEnter this to verify your account,\n\nMake sure you copy the correct code"

    message = MIMEText(body)
    message["Subject"] = "Verification Code"
    message["From"] = sender_email
    message["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)
        print("✅ Email sent to:", to_email)
    except Exception as e:
        print("❌ Email sending failed:", e)

# --- Registration Routes ---

@app.route("/register_student", methods=["GET", "POST"])
def register_student():
    if request.method == "POST":
        data = request.form
        password = data.get("initialPassword")
        confirm_password = data.get("finalPassword")

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("register_student"))

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO students (lastname, firstname, username, email, dob, gender, currentClass, password)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get("Lastname"), data.get("Firstname"), data.get("Username"),
                data.get("email"), data.get("DOB"), data.get("gender"),
                data.get("class"), password
            ))
            conn.commit()
        except sqlite3.IntegrityError:
            flash("Username or email already exists.")
            return redirect(url_for("register_student"))
        finally:
            conn.close()

        # Generate and send code
        code = str(random.randint(100000, 999999))
        session["verification_code"] = code
        session["user_email"] = data.get("email")
        session["user_role"] = "student"
        send_verification_email(data.get("email"), code)

        return redirect(url_for("verify_email"))

    return render_template("register/register_student.html")

@app.route("/register_teacher", methods=["GET", "POST"])
def register_teacher():
    if request.method == "POST":
        data = request.form
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("register_teacher"))

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO teacher (fullname, username, email, dob, gender, phoneNumber, subject, password)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get("fullname"), data.get("username"), data.get("email"), data.get("dob"),
                data.get("gender"), data.get("phone"), data.get("subject"), password
            ))
            conn.commit()
        except sqlite3.IntegrityError:
            flash("Username, email or phone number already exists.")
            return redirect(url_for("register_teacher"))
        finally:
            conn.close()

        code = str(random.randint(100000, 999999))
        session["verification_code"] = code
        session["user_email"] = data.get("email")
        session["user_role"] = "teacher"
        send_verification_email(data.get("email"), code)

        return redirect(url_for("verify_email"))

    return render_template("register/register_teacher.html")

@app.route("/register_admin", methods=["GET", "POST"])
def register_admin():
    if request.method == "POST":
        data = request.form
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("register_admin"))

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO admin (fullname, username, email, dob, gender, phoneNumber, role, password)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get("fullname"), data.get("username"), data.get("email"), data.get("dob"),
                data.get("gender"), data.get("phone"), data.get("role"), password
            ))
            conn.commit()
        except sqlite3.IntegrityError:
            flash("Username, email or phone already exists.")
            return redirect(url_for("register_admin"))
        finally:
            conn.close()

        code = str(random.randint(100000, 999999))
        session["verification_code"] = code
        session["user_email"] = data.get("email")
        session["user_role"] = "admin"
        send_verification_email(data.get("email"), code)

        return redirect(url_for("verify_email"))

    return render_template("register/register_admin.html")

# --- Email Verification ---
@app.route("/verify-email", methods=["GET", "POST"])
def verify_email():
    if request.method == "GET":
        return render_template("register/verify_email.html")

    if request.method == "POST":
        data = request.get_json()
        code_entered = data.get("code")
        correct_code = session.get("verification_code")
        email = session.get("user_email")
        role = session.get("user_role")

        if code_entered != correct_code:
            return jsonify({"success": False, "message": "❌ Incorrect code."})

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if role == "student":
            cursor.execute("UPDATE students SET verified = 1 WHERE email = ?", (email,))
            cursor.execute("SELECT id, currentClass FROM students WHERE email = ?", (email,))
            result = cursor.fetchone()
            class_map = {"jss1": "JS1", "jss2": "JS2", "jss3": "JS3", "sss1": "SS1", "sss2": "SS2", "sss3": "SS3"}
            class_code = class_map.get(result[1].lower(), "XX")
            user_id = f"STU-{class_code}-{str(result[0]).zfill(4)}"

        elif role == "teacher":
            cursor.execute("UPDATE teacher SET verified = 1 WHERE email = ?", (email,))
            cursor.execute("SELECT id FROM teacher WHERE email = ?", (email,))
            result = cursor.fetchone()
            user_id = f"TCH-{str(result[0]).zfill(4)}"

        elif role == "admin":
            cursor.execute("UPDATE admin SET verified = 1 WHERE email = ?", (email,))
            cursor.execute("SELECT id FROM admin WHERE email = ?", (email,))
            result = cursor.fetchone()
            user_id = f"ADM-{str(result[0]).zfill(4)}"

        else:
            return jsonify({"success": False, "message": "Unrecognized role."})

        conn.commit()
        conn.close()

        return jsonify({
            "success": True,
            "id": user_id,
            "redirect": url_for("login_page")
        })

# --- Dummy Login Page ---
@app.route("/login")
def login_page():
    return render_template("features/login_page.html")

# --- Run App ---
if __name__ == "__main__":
    init_db()
    app.run(debug=True)