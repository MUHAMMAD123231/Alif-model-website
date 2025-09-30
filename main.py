from flask import Flask, render_template, request, url_for, redirect, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash,check_password_hash
import sqlite3
import uuid
import random


app = Flask(__name__, template_folder="templates")
app.secret_key = "abdulsobur#muhammad"
socketio = SocketIO(app)

#----setting --- the --- config --- gmail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "akereleoluwanifemi26@gmail.com"
app.config["MAIL_PASSWORD"] = "kgvy yskr leuk qgdc"

#initialize the MAIL
mail = Mail(app)

#create a function to send Mail
def verification_code(email):
    code = random.randint(100000, 999999)
    session["verify_code"] = str(code)
    session["user_email"] = email

    #create massage body
    Gmail_msg = Message("Alif Model Group Of School",
                        sender=app.config["MAIL_USERNAME"],
                        recipients=[email])
    Gmail_msg.body = f"""You are welcome to Alif Model College Website.

Kindly enter the verification code below to continue your registration:

Verification Code: {code}

Thank you!
"""
    mail.send(Gmail_msg)

# creating invitation code for all type of user
invitationCode = {
    "admin": ["ADYYE-ADM//2C2C", "RRT*#&MM2", "ADM(A33(", "2B3BKS6BW8"],
    "guest": ["HEHE698W", "HSHHWY28", "C90BW582", "VS-+S792", "12GUST66YEU"],
    "teacher": ["TCH/737/EE", "TCH/77/99/ER", "TCH-990#GE", "A-TCH/636/EC", "AHSH/88/YEY"],
    "student": ["STU/637/ERH", "ADN/STU/3737", "STU-3Y-YEYE6", "STU+636/HSU", "CSP/ITS/629"]
}

#FUCTION TO CHECK IF THE CODE MATCHES user
def invites(code, user_type):
    return code in invitationCode.get(user_type, [])


# ---- index file ----g
@app.route("/")
def index():
    return render_template("index.html")


# ----- register admin ----
@app.route("/register/register_admin", methods=["GET", "POST"])
def register_admin():
    if request.method == "GET":
        return render_template("register/register_admin.html")

    #Geting admin info from  --form--#
    fullname = request.form.get("fullname")
    username = request.form.get("username")
    email = request.form.get("email")
    dob = request.form.get("dob")
    gender = request.form.get("gender")
    phone = request.form.get("phone")
    role = request.form.get("role")
    password = request.form.get("password")
    #-- Done getting the info ---#

    #checking invitation code
    invitation_code = request.form.get("invitation_code", "").strip()
    invitation_code = request.form.get("invitation_code", "").strip()
    if not invitation_code or not invites(invitation_code, "admin"):
      return render_template("register/register_admin.html", error="That is an Invalid invitation code. Kindly contact us.")


    #hash user password before storing
    hashPassword = generate_password_hash(password)

    #Get admin special / pass ID
    adminId = "ALIF/ADM/" + uuid.uuid4().hex[:4].upper()

    #saving to database..............
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    #check if username is not the same to avoid error
    cursor.execute("SELECT * FROM admins WHERE username = ?", (username,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return """
        <script>
        alert("username alread exit , choose or create new one")
        window.location.href = "/register/register_admin"
        </script>
        """

    #execute cursor
    cursor.execute("""
        INSERT INTO admins(fullname,username,email,dob,gender,phone,role,password,adminId)
        VALUES(?,?,?,?,?,?,?,?,?)
    """, (fullname, username, email, dob, gender, phone, role, hashPassword, adminId))
    conn.commit()
    conn.close()

    #calling the email message
    verification_code(email)
    return redirect("/register/verify_email")


# ----- register teacher ----
@app.route("/register/register_teacher", methods=["GET", "POST"])
def register_teacher():
    if request.method == "GET":
        return render_template("register/register_teacher.html")

    #Geting teachers info from  --form
    fullname = request.form.get("fullname")
    username = request.form.get("username")
    email = request.form.get("email")
    dob = request.form.get("dob")
    gender = request.form.get("gender")
    phone = request.form.get("phone")
    subject = request.form.getlist("subjects[]")
    subject_choose = ",".join(subject)
    password = request.form.get("password")
    #-- Done getting the info ---#
    #checking invitation code
    invitation_code = request.form.get("invitation_code", "").strip()
    invitation_code = request.form.get("invitation_code", "").strip()
    if not invitation_code or not invites(invitation_code, "teacher"):
      return render_template("register/register_teacher.html", error="That is an Invalid invitation code. Kindly contact us.")


    #hash user password before storing
    hashPassword = generate_password_hash(password)

    #Get teacher special / pass ID
    teacherId = "ALIF/TCH/" + uuid.uuid4().hex[:4].upper()

    #saving to database..............
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    #check if username is not the same to avoid error
    cursor.execute("SELECT * FROM teachers WHERE username = ?", (username,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return """
        <script>
        alert("username alread exit , choose or create new one")
        window.location.href = "/register/register_teacher"
        </script>
        """

    #execute cursor
    cursor.execute("""
        INSERT INTO teachers(fullname,username,email,dob,gender,phone,subject,password,teacherId)
        VALUES(?,?,?,?,?,?,?,?,?)
    """, (fullname, username, email, dob, gender, phone, subject_choose, hashPassword, teacherId))
    conn.commit()
    conn.close()

    #calling the email message
    verification_code(email)
    return redirect("/register/verify_email")


# ----- register student ----
@app.route("/register/register_student", methods=["GET", "POST"])
def register_student():
    if request.method == "GET":
        return render_template("register/register_student.html")

    #Geting student info from  --form
    lastname = request.form.get("Lastname")
    firstname = request.form.get("Firstname")
    username = request.form.get("Username")
    email = request.form.get("email")
    dob = request.form.get("DOB")
    gender = request.form.get("gender")
    Class = request.form.get("class")
    password = request.form.get("initialPassword")
    #-- Done getting the info ---#

    #checking invitation code
    invitation_code = request.form.get("invitation_code", "").strip()
    if not invitation_code or not invites(invitation_code, "student"):
      return render_template("register/register_student.html", error="That is an Invalid invitation code. Kindly contact us.")

    #hash user password before storing
    hashPassword = generate_password_hash(password)

    #Get student special / pass ID
    studentId = "ALIF/STU/" + uuid.uuid4().hex[:4].upper()

    #saving to database..............
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    #check if username is not the same to avoid error
    cursor.execute("SELECT * FROM students WHERE username = ?", (username,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return """
        <script>
        alert("username alread exit , choose or create new one")
        window.location.href = "/register/register_student"
        </script>
        """

    #execute cursor
    cursor.execute("""
        INSERT INTO students(lastname,firstname,username,email,dob,gender,class,password,studentId)
        VALUES(?,?,?,?,?,?,?,?,?)
    """, (lastname, firstname, username, email, dob, gender, Class, hashPassword, studentId))
    conn.commit()
    conn.close()

    #calling the email message
    verification_code(email)
    return redirect("/register/verify_email")


# ----- verify email -----—
@app.route("/register/verify_email", methods=["GET", "POST"])
def verify_email():
    if request.method == "POST":
        user_code = request.form.get("code")
        actual_code = session.get("verify_code")
        user_email = session.get("user_email")

        if user_code == actual_code:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            user_id = None

            # Check student
            cursor.execute("SELECT studentId FROM students WHERE email = ?", (user_email,))
            student = cursor.fetchone()
            if student:
                user_id = student[0]
                cursor.execute("UPDATE students SET verified = 1 WHERE email = ?", (user_email,))
            else:
                # Check teacher
                cursor.execute("SELECT teacherId FROM teachers WHERE email = ?", (user_email,))
                teacher = cursor.fetchone()
                if teacher:
                    user_id = teacher[0]
                    cursor.execute("UPDATE teachers SET verified = 1 WHERE email = ?", (user_email,))
                else:
                    # Check admin
                    cursor.execute("SELECT adminId FROM admins WHERE email = ?", (user_email,))
                    admin = cursor.fetchone()
                    if admin:
                        user_id = admin[0]
                        cursor.execute("UPDATE admins SET verified = 1 WHERE email = ?", (user_email,))

            conn.commit()
            conn.close()

            # Show success with user ID
            return f"""
            <script>
              alert("Email verified successfully!\\nYour ID: {user_id}\\nKeep it safe.");
              window.location.href = "/features/login_page";
            </script>
            """

        else:
            # Wrong code
            return """
            <script>
              alert("Incorrect verification code. Please try again.");
              window.location.href = "/register/verify_email";
            </script>
            """

    return render_template("register/verify_email.html")

#-- login page --
@app.route("/features/login_page", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("features/login_page.html")

    # DEBUG: Check form values
    user_id = request.form.get("user_id", "").strip()
    password = request.form.get("password", "").strip()
    invitation_code = request.form.get("invitation_code", "").strip()

    print("user_id:", user_id)
    print("password:", password)
    print("invitation_code:", invitation_code)

    # Guest Login
    if user_id == "" and password == "" and invitation_code:
        if invites(invitation_code, "guest"):
            session["user_role"] = "guest"
            return redirect("/dashboard/guest_dashboard")
        else:
            print("Guest code invalid.")
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

        # Student
        cursor.execute("SELECT password FROM students WHERE studentId = ?", (user_id,))
        student = cursor.fetchone()
        if student and check_password_hash(student[0], password):
            session["user_role"] = "student"
            session["user_id"] = user_id
            conn.close()
            return redirect("/dashboard/student_dashboard")

        # Teacher
        cursor.execute("SELECT password FROM teachers WHERE teacherId = ?", (user_id,))
        teacher = cursor.fetchone()
        if teacher and check_password_hash(teacher[0], password):
            session["user_role"] = "teacher"
            session["user_id"] = user_id
            conn.close()
            return redirect("/dashboard/teacher_dashboard")

        # Admin
        cursor.execute("SELECT password FROM admins WHERE adminId = ?", (user_id,))
        admin = cursor.fetchone()
        if admin and check_password_hash(admin[0], password):
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

    else:
        return """
        <script>
        alert("Please fill in the required fields.");
        window.location.href = '/features/login_page';
        </script>
        """

#-- classroom page --

# --& Jss1 ---&
@app.route("/classroom/discussion_jss1")
def jss1():
    user_role = session.get("user_role")
    user_id = session.get("user_id")
    username = None
    room = "jss1"
    if user_role == "student":
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT firstname, lastname, class FROM students WHERE studentId = ?", (user_id,))
        student = cursor.fetchone()
        if student:
            username = f"{student[0]} {student[1]}"
            room = student[2].lower() if student[2] else room
        conn.close()
    elif user_role == "teacher":
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT fullname, subject FROM teachers WHERE teacherId = ?", (user_id,))
        teacher = cursor.fetchone()
        if teacher:
            username = teacher[0]
        conn.close()
    elif user_role == "admin":
        username = "Admin"
    else:
        return redirect(url_for('login'))
    return render_template("classroom/discussion_jss1.html", chat_username=username, chat_room=room, user_role=user_role)

# --& Jss2 ---&
@app.route("/classroom/discussion_jss2")
def jss2():
    # Same logic as jss1, but room = "jss2"
    user_role = session.get("user_role")
    user_id = session.get("user_id")
    username = None
    room = "jss2"
    if user_role == "student":
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT firstname, lastname, class FROM students WHERE studentId = ?", (user_id,))
        student = cursor.fetchone()
        if student:
            username = f"{student[0]} {student[1]}"
            room = student[2].lower() if student[2] else room
        conn.close()
    elif user_role == "teacher":
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT fullname, subject FROM teachers WHERE teacherId = ?", (user_id,))
        teacher = cursor.fetchone()
        if teacher:
            username = teacher[0]
        conn.close()
    elif user_role == "admin":
        username = "Admin"
    else:
        return redirect(url_for('login'))
    return render_template("classroom/discussion_jss2.html", chat_username=username, chat_room=room, user_role=user_role)

# --& Jss3 ---&
@app.route("/classroom/discussion_jss3")
def jss3():
    user_role = session.get("user_role")
    user_id = session.get("user_id")
    username = None
    room = "jss3"
    if user_role == "student":
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT firstname, lastname, class FROM students WHERE studentId = ?", (user_id,))
        student = cursor.fetchone()
        if student:
            username = f"{student[0]} {student[1]}"
            room = student[2].lower() if student[2] else room
        conn.close()
    elif user_role == "teacher":
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT fullname, subject FROM teachers WHERE teacherId = ?", (user_id,))
        teacher = cursor.fetchone()
        if teacher:
            username = teacher[0]
        conn.close()
    elif user_role == "admin":
        username = "Admin"
    else:
        return redirect(url_for('login'))
    return render_template("classroom/discussion_jss3.html", chat_username=username, chat_room=room, user_role=user_role)

# --& sss1 ---&
@app.route("/classroom/discussion_sss1")
def sss1():
    user_role = session.get("user_role")
    user_id = session.get("user_id")
    username = None
    room = "sss1"
    if user_role == "student":
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT firstname, lastname, class FROM students WHERE studentId = ?", (user_id,))
        student = cursor.fetchone()
        if student:
            username = f"{student[0]} {student[1]}"
            room = student[2].lower() if student[2] else room
        conn.close()
    elif user_role == "teacher":
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT fullname, subject FROM teachers WHERE teacherId = ?", (user_id,))
        teacher = cursor.fetchone()
        if teacher:
            username = teacher[0]
        conn.close()
    elif user_role == "admin":
        username = "Admin"
    else:
        return redirect(url_for('login'))
    return render_template("classroom/discussion_sss1.html", chat_username=username, chat_room=room, user_role=user_role)

# --& sss2 ---&
@app.route("/classroom/discussion_sss2")
def sss2():
    user_role = session.get("user_role")
    user_id = session.get("user_id")
    username = None
    room = "sss2"
    if user_role == "student":
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT firstname, lastname, class FROM students WHERE studentId = ?", (user_id,))
        student = cursor.fetchone()
        if student:
            username = f"{student[0]} {student[1]}"
            room = student[2].lower() if student[2] else room
        conn.close()
    elif user_role == "teacher":
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT fullname, subject FROM teachers WHERE teacherId = ?", (user_id,))
        teacher = cursor.fetchone()
        if teacher:
            username = teacher[0]
        conn.close()
    elif user_role == "admin":
        username = "Admin"
    else:
        return redirect(url_for('login'))
    return render_template("classroom/discussion_sss2.html", chat_username=username, chat_room=room, user_role=user_role)

# --& sss3 ---&
@app.route("/classroom/discussion_sss3")
def sss3():
    user_role = session.get("user_role")
    user_id = session.get("user_id")
    username = None
    room = "sss3"
    if user_role == "student":
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT firstname, lastname, class FROM students WHERE studentId = ?", (user_id,))
        student = cursor.fetchone()
        if student:
            username = f"{student[0]} {student[1]}"
            room = student[2].lower() if student[2] else room
        conn.close()
    elif user_role == "teacher":
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT fullname, subject FROM teachers WHERE teacherId = ?", (user_id,))
        teacher = cursor.fetchone()
        if teacher:
            username = teacher[0]
        conn.close()
    elif user_role == "admin":
        username = "Admin"
    else:
        return redirect(url_for('login'))
    return render_template("classroom/discussion_sss3.html", chat_username=username, chat_room=room, user_role=user_role)


# --& admin dashboard ---&
@app.route("/dashboard/admin_dashboard")
def admin_dashboard():
    return render_template("dashboard/admin_dashboard.html")

# --& teacher dashboard ---&
@app.route("/dashboard/teacher_dashboard")
def teacher_dashboard():
    return render_template("dashboard/teacher_dashboard.html")

# --& student dashboard ---&
@app.route("/dashboard/student_dashboard")
def student_dashboard():
    user_id = session.get("user_id")
    class_forum = None
    if user_id:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT class FROM students WHERE studentId = ?", (user_id,))
        result = cursor.fetchone()
        if result and result[0]:
            class_forum = result[0].lower()
        conn.close()
    return render_template("dashboard/student_dashboard.html", class_forum=class_forum)

# --& guest dashboard ---&
@app.route("/dashboard/guest_dashboard")
def guest_dashboard():
    return render_template("dashboard/guest_dashboard.html")


@socketio.on('join')
def handle_join(data):
    room = data.get('room')
    username = data.get('username')
    join_room(room)
    emit('status', {'msg': f'{username} has joined the chat.'}, room=room)

@socketio.on('leave')
def handle_leave(data):
    room = data.get('room')
    username = data.get('username')
    leave_room(room)
    emit('status', {'msg': f'{username} has left the chat.'}, room=room)

@socketio.on('send_message')
def handle_send_message(data):
    room = data.get('room')
    username = data.get('username')
    message = data.get('message')
    emit('receive_message', {'username': username, 'message': message}, room=room)

if __name__ == "__main__":
    socketio.run(app, debug=True)