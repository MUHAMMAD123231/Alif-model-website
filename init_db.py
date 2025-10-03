# ---- School Database ---- #
import sqlite3

# Connect to database file (auto-create if not exists)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# ---------------- Students ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  lastname TEXT NOT NULL,
  firstname TEXT NOT NULL,
  username TEXT NOT NULL UNIQUE,
  email TEXT NOT NULL,
  dob TEXT NOT NULL,
  gender TEXT NOT NULL,
  Class TEXT NOT NULL,
  password TEXT NOT NULL,
  studentId TEXT NOT NULL UNIQUE,
  verified INTEGER DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# ---------------- Teachers ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS teachers(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fullname TEXT NOT NULL,
  username TEXT NOT NULL UNIQUE,
  email TEXT NOT NULL,
  dob TEXT NOT NULL,
  gender TEXT NOT NULL,
  phone TEXT NOT NULL,
  subject TEXT NOT NULL,
  password TEXT NOT NULL,
  teacherId TEXT NOT NULL UNIQUE,
  verified INTEGER DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# ---------------- Admins ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS admins(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fullname TEXT NOT NULL,
  username TEXT NOT NULL UNIQUE,
  email TEXT NOT NULL,
  dob TEXT NOT NULL,
  gender TEXT NOT NULL,
  phone TEXT NOT NULL,
  role TEXT NOT NULL,
  password TEXT NOT NULL,
  adminId TEXT NOT NULL UNIQUE,
  verified INTEGER DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# ---------------- Student Biodata ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS biodata(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL,

  -- Personal Info
  fullname TEXT,
  dob TEXT,
  gender TEXT,
  nationality TEXT,
  state_of_origin TEXT,
  lga TEXT,
  photo TEXT, -- file path / filename

  -- Contact & Address
  street TEXT,
  city TEXT,
  state TEXT,
  landmark TEXT,
  phone TEXT,
  email TEXT,

  -- Primary Guardian
  guardian_name TEXT,
  guardian_relationship TEXT,
  guardian_phone1 TEXT,
  guardian_phone2 TEXT,
  guardian_email TEXT,
  guardian_occupation TEXT,
  guardian_address TEXT,

  -- Secondary Guardian
  guardian2_name TEXT,
  guardian2_relationship TEXT,
  guardian2_phone TEXT,
  guardian2_email TEXT,
  guardian2_occupation TEXT,

  -- Emergency Contact
  emergency_name TEXT,
  emergency_relation TEXT,
  emergency_phone TEXT,

  -- Health Info
  blood_group TEXT,
  genotype TEXT,
  allergies TEXT,
  conditions TEXT,
  special_needs TEXT,

  -- Academic Background
  last_school TEXT,
  school_address TEXT,
  class_completed TEXT,
  leaving_reason TEXT,

  -- Interests
  hobbies TEXT,
  clubs TEXT,

  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE
)
""")

# ---------------- Courses ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS courses(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  course_code TEXT NOT NULL,
  course_name TEXT NOT NULL,
  class_level TEXT NOT NULL,
  teacher_id INTEGER,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(teacher_id) REFERENCES teachers(id)
)
""")

# ---------------- Assignments ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS assignments(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  due_date TEXT NOT NULL,
  course_id INTEGER NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(course_id) REFERENCES courses(id)
)
""")

# ---------------- Submissions ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS submissions(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  assignment_id INTEGER NOT NULL,
  student_id INTEGER NOT NULL,
  content TEXT,
  submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(assignment_id) REFERENCES assignments(id),
  FOREIGN KEY(student_id) REFERENCES students(id)
)
""")

# ---------------- Results / Grades ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS results(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL,
  course_id INTEGER NOT NULL,
  score REAL,
  grade TEXT,
  teacher_comment TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(student_id) REFERENCES students(id),
  FOREIGN KEY(course_id) REFERENCES courses(id)
)
""")

# ---------------- Attendance ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL,
  date TEXT NOT NULL,
  status TEXT NOT NULL, -- Present, Absent, Late
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(student_id) REFERENCES students(id)
)
""")

# ---------------- Announcements / School Feed ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS announcements(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  message TEXT NOT NULL,
  created_by TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Save & close
conn.commit()
conn.close()

print("✅ Database initialized successfully with all tables.")