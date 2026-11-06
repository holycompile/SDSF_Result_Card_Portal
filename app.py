import os
from flask import Flask, render_template, redirect, url_for, request, flash
from dotenv import load_dotenv
from databases.query import enter_student_info, create_table, checking_enroll_no

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "random_secret_key_sdsf_2026")

# Ensure table exists upon app initialization
create_table()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/insert_student/info_hit")
def info_hit():
    msg = request.args.get("msg")
    return render_template("info_hit.html", msg=msg)

@app.route("/insert_student", methods=["POST", "GET"])
def insert_student():
    if request.method == "POST":
        enroll_no = request.form.get("enroll_no")
        if checking_enroll_no(enroll_no):
            return redirect(url_for("info_hit", msg="student exists"))
        else:
            sname = request.form.get("sname")
            course = request.form.get("course")
            start_batch = request.form.get("start-batch")
            end_batch = request.form.get("end-batch")
            semester = request.form.get("semester")
            rollno = request.form.get("rollno")
            exam = request.form.get("exam")
            father = request.form.get("father")
            mother = request.form.get("mother")

            enter_student_info(
                sname, course, start_batch, end_batch, semester,
                enroll_no, rollno, exam, father, mother
            )
            return redirect(url_for("info_hit", msg="success"))

    return render_template("forms/insert_student.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
