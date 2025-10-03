from flask import Blueprint, render_template, session, redirect, url_for
import sqlite3

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route("/dashboard/admin_dashboard")
def admin_dashboard():
    return render_template("dashboard/admin_dashboard.html")

@dashboard_bp.route("/dashboard/teacher_dashboard")
def teacher_dashboard():
    return render_template("dashboard/teacher_dashboard.html")

@dashboard_bp.route("/dashboard/student_dashboard")
def student_dashboard():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Fetch student info
    cursor.execute("SELECT id, firstname, lastname, email, class FROM students WHERE studentId = ?", (user_id,))
    student = cursor.fetchone()

    if not student:
        conn.close()
        return "Student account not found", 404

    student_pk = student["id"]

    # Fetch existing biodata if available
    cursor.execute("SELECT * FROM biodata WHERE student_id = ?", (student_pk,))
    biodata = cursor.fetchone()
    if not biodata:
        biodata = {}  # fallback to prevent template errors

    conn.close()

    # Prepare class forum for sidebar
    student_class = student["class"].lower() if student["class"] else None

    return render_template(
        "dashboard/student_dashboard.html",
        student=student,
        biodata=biodata,
        class_forum=student_class
    )

@dashboard_bp.route("/dashboard/guest_dashboard")
def guest_dashboard():
    return render_template("dashboard/guest_dashboard.html")
