from flask import Blueprint, render_template, request, redirect, session, url_for
import sqlite3, uuid, random
from app import mail
from flask_mail import Message

auth_bp = Blueprint("auth", __name__)

# --- Helper: send verification code ---
def verification_code(email):
    code = random.randint(100000, 999999)
    session["verify_code"] = str(code)
    session["user_email"] = email

    Gmail_msg = Message("Alif Model Group Of School",
                        sender="akereleoluwanifemi26@gmail.com",
                        recipients=[email])
    Gmail_msg.body = f"""You are welcome to Alif Model College Website.

Kindly enter the verification code below to continue your registration:

Verification Code: {code}

Thank you!
"""
    mail.send(Gmail_msg)


# --- Invitation codes ---
invitationCode = {
    "admin": ["ADYYE-ADM//2C2C", "RRT*#&MM2", "ADM(A33(", "2B3BKS6BW8"],
    "guest": ["HEHE698W", "HSHHWY28", "C90BW582", "VS-+S792", "12GUST66YEU"],
    "teacher": ["TCH/737/EE", "TCH/77/99/ER", "TCH-990#GE", "A-TCH/636/EC", "AHSH/88/YEY"],
    "student": ["STU/637/ERH", "ADN/STU/3737", "STU-3Y-YEYE6", "STU+636/HSU", "CSP/ITS/629"]
}

def invites(code, user_type):
    return code in invitationCode.get(user_type, [])


# ----- Register Admin -----
@auth_bp.route("/register/register_admin", methods=["GET", "POST"])
def register_admin():
    if request.method == "GET":
        return render_template("register/register_admin.html")

    fullname = request.form.get("fullname")
    username = request.form.get("username")
    email = request.form.get("email")
    dob = request.form.get("dob")
    gender = request.form.get("gender")
    phone = request.form.get("phone")
    role = request.form.get("role")
    password = request.form.get("password")

    invitation_code = request.form.get("invitation_code", "").strip()
    if not invitation_code or not invites(invitation_code, "admin"):
        return render_template("register/register_admin.html", error="That is an Invalid invitation code. Kindly contact us.")

    adminId = "ALIF/ADM/" + uuid.uuid4().hex[:4].upper()

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins WHERE username = ?", (username,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return """
        <script>
        alert("username already exists, choose a new one");
        window.location.href = "/register/register_admin"
        </script>
        """

    cursor.execute("""
        INSERT INTO admins(fullname,username,email,dob,gender,phone,role,password,adminId)
        VALUES(?,?,?,?,?,?,?,?,?)
    """, (fullname, username, email, dob, gender, phone, role, password, adminId))
    conn.commit()
    conn.close()

    verification_code(email)
    return redirect("/register/verify_email")


# ----- Register Teacher -----
@auth_bp.route("/register/register_teacher", methods=["GET", "POST"])
def register_teacher():
    if request.method == "GET":
        return render_template("register/register_teacher.html")

    fullname = request.form.get("fullname")
    username = request.form.get("username")
    email = request.form.get("email")
    dob = request.form.get("dob")
    gender = request.form.get("gender")
    phone = request.form.get("phone")
    subject = request.form.getlist("subjects[]")
    subject_choose = ",".join(subject)
    password = request.form.get("password")

    invitation_code = request.form.get("invitation_code", "").strip()
    if not invitation_code or not invites(invitation_code, "teacher"):
        return render_template("register/register_teacher.html", error="That is an Invalid invitation code. Kindly contact us.")

    teacherId = "ALIF/TCH/" + uuid.uuid4().hex[:4].upper()

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teachers WHERE username = ?", (username,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return """
        <script>
        alert("username already exists, choose a new one");
        window.location.href = "/register/register_teacher"
        </script>
        """

    cursor.execute("""
        INSERT INTO teachers(fullname,username,email,dob,gender,phone,subject,password,teacherId)
        VALUES(?,?,?,?,?,?,?,?,?)
    """, (fullname, username, email, dob, gender, phone, subject_choose, password, teacherId))
    conn.commit()
    conn.close()

    verification_code(email)
    return redirect("/register/verify_email")


# ----- Register Student -----
@auth_bp.route("/register/register_student", methods=["GET", "POST"])
def register_student():
    if request.method == "GET":
        return render_template("register/register_student.html")

    lastname = request.form.get("Lastname")
    firstname = request.form.get("Firstname")
    username = request.form.get("Username")
    email = request.form.get("email")
    dob = request.form.get("DOB")
    gender = request.form.get("gender")
    Class = request.form.get("class")
    password = request.form.get("initialPassword")

    invitation_code = request.form.get("invitation_code", "").strip()
    if not invitation_code or not invites(invitation_code, "student"):
        return render_template("register/register_student.html", error="That is an Invalid invitation code. Kindly contact us.")

    studentId = "ALIF/STU/" + uuid.uuid4().hex[:4].upper()

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE username = ?", (username,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return """
        <script>
        alert("username already exists, choose a new one");
        window.location.href = "/register/register_student"
        </script>
        """

    cursor.execute("""
        INSERT INTO students(lastname,firstname,username,email,dob,gender,class,password,studentId)
        VALUES(?,?,?,?,?,?,?,?,?)
    """, (lastname, firstname, username, email, dob, gender, Class, password, studentId))
    conn.commit()
    conn.close()

    verification_code(email)
    return redirect("/register/verify_email")


# ----- Verify Email -----
@auth_bp.route("/register/verify_email", methods=["GET", "POST"])
def verify_email():
    if request.method == "POST":
        user_code = request.form.get("code")
        actual_code = session.get("verify_code")
        user_email = session.get("user_email")

        if user_code == actual_code:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            user_id = None

            cursor.execute("SELECT studentId FROM students WHERE email = ?", (user_email,))
            student = cursor.fetchone()
            if student:
                user_id = student[0]
                cursor.execute("UPDATE students SET verified = 1 WHERE email = ?", (user_email,))
            else:
                cursor.execute("SELECT teacherId FROM teachers WHERE email = ?", (user_email,))
                teacher = cursor.fetchone()
                if teacher:
                    user_id = teacher[0]
                    cursor.execute("UPDATE teachers SET verified = 1 WHERE email = ?", (user_email,))
                else:
                    cursor.execute("SELECT adminId FROM admins WHERE email = ?", (user_email,))
                    admin = cursor.fetchone()
                    if admin:
                        user_id = admin[0]
                        cursor.execute("UPDATE admins SET verified = 1 WHERE email = ?", (user_email,))

            conn.commit()
            conn.close()

            return f"""
            <script>
              alert("Email verified successfully!\\nYour ID: {user_id}\\nKeep it safe.");
              window.location.href = "/features/login_page";
            </script>
            """

        return """
        <script>
          alert("Incorrect verification code. Please try again.");
          window.location.href = "/register/verify_email";
        </script>
        """

    return render_template("register/verify_email.html")


# ----- Login -----
@auth_bp.route("/features/login_page", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("features/login_page.html")

    user_id = request.form.get("user_id", "").strip()
    password = request.form.get("password", "").strip()
    invitation_code = request.form.get("invitation_code", "").strip()

    # Guest Login
    if user_id == "" and password == "" and invitation_code:
        if invites(invitation_code, "guest"):
            session["user_role"] = "guest"
            return redirect("/dashboard/guest_dashboard")
        return """
        <script>
        alert("Invalid guest invitation code.");
        window.location.href = '/features/login_page';
        </script>
        """

    # Normal Login
    elif user_id and password:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM students WHERE studentId = ?", (user_id,))
        student = cursor.fetchone()
        if student and student[0] == password:
            session["user_role"] = "student"
            session["user_id"] = user_id
            conn.close()
            return redirect("/dashboard/student_dashboard")

        cursor.execute("SELECT password FROM teachers WHERE teacherId = ?", (user_id,))
        teacher = cursor.fetchone()
        if teacher and teacher[0] == password:
            session["user_role"] = "teacher"
            session["user_id"] = user_id
            conn.close()
            return redirect("/dashboard/teacher_dashboard")

        cursor.execute("SELECT password FROM admins WHERE adminId = ?", (user_id,))
        admin = cursor.fetchone()
        if admin and admin[0] == password:
            session["user_role"] = "admin"
            session["user_id"] = user_id
            conn.close()
            return redirect("/dashboard/admin_dashboard")

        conn.close()
        return """
        <script>
        alert("Invalid ID or password.");
        window.location.href = '/features/login_page';
        </script>
        """

    return """
    <script>
    alert("Please fill in the required fields.");
    window.location.href = '/features/login_page';
    </script>
    """
