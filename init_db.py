#----School Database ----#

import sqlite3

#Connect to my database file
conn = sqlite3.connect("database.db")

#make a pen
cursor = conn.cursor()

#create student table

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


#create teacher table

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


#create admin table

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