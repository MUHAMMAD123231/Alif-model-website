import os
import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename

student_bio_bp = Blueprint("student_bio", __name__, url_prefix="/dashboard")

ALLOWED_EXT = {"png", "jpg", "jpeg", "gif"}

def allowed_file(fname):
    return "." in fname and fname.rsplit(".", 1)[1].lower() in ALLOWED_EXT

@student_bio_bp.route("/biodata", methods=["GET", "POST"])
def biodata():
    # Ensure student is logged in
    if session.get("user_role") != "student" or not session.get("user_id"):
        return redirect("/features/login_page")

    student_external_id = session.get("user_id")

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Get student info
    cur.execute("SELECT id, firstname, lastname, email, class FROM students WHERE studentId = ?", (student_external_id,))
    student_row = cur.fetchone()
    if not student_row:
        conn.close()
        return "Student account not found", 404

    student_pk = student_row["id"]

    if request.method == "POST":
        # ---------------- Personal Info ----------------
        fullname = f"{student_row['firstname']} {student_row['lastname']}"
        dob = request.form.get("dob", "").strip()
        gender = request.form.get("gender", "").strip()
        nationality = request.form.get("nationality", "").strip()
        state_origin = request.form.get("state_origin", "").strip()
        lga = request.form.get("lga", "").strip()

        # ---------------- Contact & Address ----------------
        street = request.form.get("street", "").strip()
        city = request.form.get("city", "").strip()
        state = request.form.get("state", "").strip()
        landmark = request.form.get("landmark", "").strip()
        phone = request.form.get("student_phone", "").strip()
        email = student_row["email"]

        # ---------------- Guardians ----------------
        guardian_name = request.form.get("guardian_name", "").strip()
        guardian_relationship = request.form.get("guardian_relationship", "").strip()
        guardian_phone1 = request.form.get("guardian_phone1", "").strip()
        guardian_phone2 = request.form.get("guardian_phone2", "").strip()
        guardian_email = request.form.get("guardian_email", "").strip()
        guardian_occupation = request.form.get("guardian_occupation", "").strip()
        guardian_address = request.form.get("guardian_address", "").strip()

        guardian2_name = request.form.get("guardian2_name", "").strip()
        guardian2_relationship = request.form.get("guardian2_relationship", "").strip()
        guardian2_phone = request.form.get("guardian2_phone", "").strip()
        guardian2_email = request.form.get("guardian2_email", "").strip()
        guardian2_occupation = request.form.get("guardian2_occupation", "").strip()

        # ---------------- Emergency Contact ----------------
        emergency_name = request.form.get("emergency_name", "").strip()
        emergency_relation = request.form.get("emergency_relation", "").strip()
        emergency_phone = request.form.get("emergency_phone", "").strip()

        # ---------------- Health Info ----------------
        blood_group = request.form.get("blood_group", "").strip()
        genotype = request.form.get("genotype", "").strip()
        allergies = request.form.get("allergies", "").strip()
        conditions = request.form.get("conditions", "").strip()
        special_needs = request.form.get("special_needs", "").strip()

        # ---------------- Academic Background ----------------
        last_school = request.form.get("last_school", "").strip()
        school_address = request.form.get("school_address", "").strip()
        class_completed = request.form.get("class_completed", "").strip()
        leaving_reason = request.form.get("leaving_reason", "").strip()

        # ---------------- Interests ----------------
        hobbies = request.form.get("hobbies", "").strip()
        clubs = request.form.get("clubs", "").strip()

        # ---------------- Photo Upload ----------------
        photo_relative = None
        file = request.files.get("passport")
        if file and file.filename and allowed_file(file.filename):
            uploads_dir = os.path.join("static", "uploads")
            os.makedirs(uploads_dir, exist_ok=True)
            safe_name = secure_filename(f"{student_external_id}_{file.filename}")
            save_path = os.path.join(uploads_dir, safe_name)
            file.save(save_path)
            photo_relative = f"uploads/{safe_name}"

        # ---------------- Insert or Update ----------------
        cur.execute("SELECT id FROM biodata WHERE student_id = ?", (student_pk,))
        exists = cur.fetchone()

        if exists:
            cur.execute("""
                UPDATE biodata SET
                    fullname=?, dob=?, gender=?, nationality=?, state_of_origin=?, lga=?, photo=?,
                    street=?, city=?, state=?, landmark=?, phone=?, email=?,
                    guardian_name=?, guardian_relationship=?, guardian_phone1=?, guardian_phone2=?, guardian_email=?, guardian_occupation=?, guardian_address=?,
                    guardian2_name=?, guardian2_relationship=?, guardian2_phone=?, guardian2_email=?, guardian2_occupation=?,
                    emergency_name=?, emergency_relation=?, emergency_phone=?,
                    blood_group=?, genotype=?, allergies=?, conditions=?, special_needs=?,
                    last_school=?, school_address=?, class_completed=?, leaving_reason=?,
                    hobbies=?, clubs=?
                WHERE student_id=?
            """, (
                fullname, dob, gender, nationality, state_origin, lga, photo_relative,
                street, city, state, landmark, phone, email,
                guardian_name, guardian_relationship, guardian_phone1, guardian_phone2, guardian_email, guardian_occupation, guardian_address,
                guardian2_name, guardian2_relationship, guardian2_phone, guardian2_email, guardian2_occupation,
                emergency_name, emergency_relation, emergency_phone,
                blood_group, genotype, allergies, conditions, special_needs,
                last_school, school_address, class_completed, leaving_reason,
                hobbies, clubs,
                student_pk
            ))
        else:
            cur.execute("""
                INSERT INTO biodata (
                    student_id, fullname, dob, gender, nationality, state_of_origin, lga, photo,
                    street, city, state, landmark, phone, email,
                    guardian_name, guardian_relationship, guardian_phone1, guardian_phone2, guardian_email, guardian_occupation, guardian_address,
                    guardian2_name, guardian2_relationship, guardian2_phone, guardian2_email, guardian2_occupation,
                    emergency_name, emergency_relation, emergency_phone,
                    blood_group, genotype, allergies, conditions, special_needs,
                    last_school, school_address, class_completed, leaving_reason,
                    hobbies, clubs
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                student_pk, fullname, dob, gender, nationality, state_origin, lga, photo_relative,
                street, city, state, landmark, phone, email,
                guardian_name, guardian_relationship, guardian_phone1, guardian_phone2, guardian_email, guardian_occupation, guardian_address,
                guardian2_name, guardian2_relationship, guardian2_phone, guardian2_email, guardian2_occupation,
                emergency_name, emergency_relation, emergency_phone,
                blood_group, genotype, allergies, conditions, special_needs,
                last_school, school_address, class_completed, leaving_reason,
                hobbies, clubs
            ))

        conn.commit()
        conn.close()
        return redirect(url_for("student_bio.biodata"))

    # GET request → load existing biodata
    cur.execute("SELECT * FROM biodata WHERE student_id = ?", (student_pk,))
    biodata = cur.fetchone()
    if not biodata:
        biodata = {}  # safe fallback for template

    conn.close()
    return render_template("dashboard/student_dashboard.html",
                           biodata=biodata,
                           student=student_row)
