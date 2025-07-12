from flask import Flask , render_template

app = Flask(__name__,template_folder="templates")

# ---- index file ----g
@app.route("/")
def index():
  return render_template("index.html")
  
  
# ----- register admin ----
@app.route("/register/register_admin",methods = ["GET","POST"])
def register_admin():
  return render_template("register/register_admin.html")
  
  
# ----- register teacher ----
@app.route("/register/register_teacher" ,methods = ["GET","POST"])
def register_teacher():
  return render_template("register/register_teacher.html")
  
  
# ----- register student ----
@app.route("/register/register_student" ,methods = ["GET","POST"])
def register_student():
  return render_template("register/register_student.html")
  

# ----- verify email -----—
@app.route("/register/verify_email" ,methods = ["GET","POST"])
def verify_email():
  return render_template("register/verify_email.html")
 
#-- login page --
@app.route("/features/login_page" ,methods = ["GET","POST"])
def all_login():
  return render_template("features/login_page.html")
  
  
#-- classroom page --

# --& Jss1 ---&
@app.route("/classroom/discussion_jss1")
def jss1():
  return render_template("classroom/discussion_jss1.html")
  
  
# --& Jss2 ---&
@app.route("/classroom/discussion_jss2")
def jss2():
  return render_template("classroom/discussion_jss2.html")
  
  
# --& Jss3 ---&
@app.route("/classroom/discussion_jss3")
def jss3():
  return render_template("classroom/discussion_jss3.html")
  
  
# --& sss1 ---&
@app.route("/classroom/discussion_sss1")
def sss1():
  return render_template("classroom/discussion_sss1.html")
  
  
# --& sss2 ---&
@app.route("/classroom/discussion_sss2")
def sss2():
  return render_template("classroom/discussion_sss2.html")
  
  
# --& sss3 ---&
@app.route("/classroom/discussion_sss3")
def sss3():
  return render_template("classroom/discussion_sss3.html")


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
  return render_template("dashboard/student_dashboard.html")


# --& guest dashboard ---&
@app.route("/dashboard/guest_dashboard")
def guest_dashboard():
  return render_template("dashboard/guest_dashboard.html")

if __name__=="__main__":
  app.run(debug = True)