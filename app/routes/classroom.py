# Classroom discussion/chat routes
from flask import Blueprint, render_template, session, redirect, url_for
import sqlite3

classroom_bp = Blueprint('classroom', __name__)

def get_username(user_role, user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    username, room = None, None

    if user_role == "student":
        cursor.execute("SELECT username, class FROM students WHERE studentId = ?", (user_id,))
        student = cursor.fetchone()
        if student:
            username, room = student[0], student[1].lower()
    elif user_role == "teacher":
        cursor.execute("SELECT username FROM teachers WHERE teacherId = ?", (user_id,))
        teacher = cursor.fetchone()
        if teacher:
            username = teacher[0]
    elif user_role == "admin":
        username = "Admin"

    conn.close()
    return username, room


# Dynamic route for all classrooms
@classroom_bp.route("/classroom/discussion_<level>")
def discussion(level):
    user_role = session.get("user_role")
    user_id = session.get("user_id")

    username, student_room = get_username(user_role, user_id)

    if not username:
        return redirect(url_for('auth.login'))  # not logged in

    valid_levels = ["jss1", "jss2", "jss3", "sss1", "sss2", "sss3"]
    if level not in valid_levels:
        return redirect(url_for('auth.login'))  # invalid class

    if user_role == "student":
        if student_room != level:
            return redirect(url_for('auth.login'))  # wrong class
        room = student_room
    else:
        room = level  # teacher/admin can open any

    class_display = level.upper().replace("SSS", "SSS ").replace("JSS", "JSS ")

    return render_template(
        "classroom/discussion_classroom.html",
        chat_username=username,
        chat_room=room,
        class_display=class_display + " Group",
        user_role=user_role
    )