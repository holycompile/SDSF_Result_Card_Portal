import os
from flask import Flask, render_template, redirect, url_for, request, flash
from dotenv import load_dotenv
from databases.query import enter_student_info, create_table, checking_enroll_no
from databases.query import view_courses,course_table



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




@app.route("/result_card", methods=['POST','GET'])
def result_card():
    student = None
    msg = None
    enroll_no = None
    course_table__=None
    if request.method == 'POST':
        enroll_no = request.form.get("enroll_no")
        if checking_enroll_no(enroll_no):
            '''
            
            By default in Python, cursor.fetchall() returns a list of tuples, where each tuple represents one database row:
            eg:
            records=[
                #  This entire tuple is records[0]
                (1, 'DE1234567', 'Joyobrata Das', 'ds', '2026', '2028', '1', 'DS7B-8978', '2026-11-01', 'Father Name', 'Mother Name', '2026-11-07 05:00:00')
            ]
            
            '''
            records = view_courses(enroll_no)
            if records:
                student = records[0] ## student is taking the value  # Grab the 1st index record as its the only value in records for now 
                table_name_rendering = ""
                if student[3]=="aids":
                    table_name_rendering="aids_sem_"+student[6]
                elif student[3]=="ds" or student[3]=="bda":
                    table_name_rendering="ds_bda_sem_"+student[6]
                elif student[3]=="exe":
                    table_name_rendering="exe_sem_"+student[6]
                elif student[3]=="msc":
                    table_name_rendering="msc_sem_"+student[6]
                else:
                    table_name_rendering="mba_sem_"+student[6]
                    
                '''
                Because it runs cursor.fetchall(), it returns a list of tuples containing all the rows (all subjects) from that semester table (e.g., ds_bda_sem_1):
                eg:
                python---
                [
                    ('DS501', 'Statistical Computing', 4),
                    ('DS502', 'Machine Learning', 4),
                    ('DS503', 'Database Management', 3)
                ]

                Each tuple inside the list is one subject in that semester.
                  
                '''
                
                course_table__= course_table(table_name_rendering)
            
            
            msg = "student_there"
        else:
            msg = "student_not_there"

        
    return render_template("result_card.html", msg=msg, enroll_no=enroll_no, student=student, course_table__=course_table__)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
