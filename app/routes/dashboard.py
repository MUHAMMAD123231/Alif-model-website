# Dashboard routes (student, teacher, admin, guest)
# - Handles dashboard views and logic for each user role
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
@dashboard_bp.route("/dashboard/student_dashboard")
def student_dashboard():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT class FROM students WHERE studentId = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    student_class = row[0].lower() if row and row[0] else None

    return render_template("dashboard/student_dashboard.html", class_forum=student_class)


@dashboard_bp.route("/dashboard/guest_dashboard")
def guest_dashboard():
	return render_template("dashboard/guest_dashboard.html")
