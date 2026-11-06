from flask import Flask 
from flask import render_template,redirect,url_for,request,flash
from databases.query import enter_student_info, create_table
import sqlite3


app = Flask(__name__)

app.secret_key = "random_secret_key_lol"

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")



@app.route("/check_enrollment_number")
def checking_enroll_no(enroll_no):
    
    connect = sqlite3.connect('databases/student_info.db')
    cursor=connect.cursor()
    cursor.execute(f"""--sql
        SELECT EXISTS (
            SELECT 1 FROM studenttable WHERE enrollment_no = "{enroll_no}"
        );
                
                """)
    exists = cursor.fetchone()[0]
    connect.close()
    return exists == 1


@app.route("/insert_student/info_hit")
def info_hit():
    msg=request.args.get('msg')
    return render_template("info_hit.html",msg=msg)


@app.route("/insert_student", methods=['POST','GET'])
def insert_student():
    
    if request.method=='POST':
        create_table()
        enroll_no = request.form.get('enroll_no')
        if checking_enroll_no(enroll_no):
            return redirect (url_for("info_hit",msg="student exists"))
        else:
            sname = request.form.get('sname')
            course = request.form.get('course')
            start_batch = request.form.get('start-batch')
            end_batch = request.form.get('end-batch')
            semester = request.form.get('semester')
            
            rollno = request.form.get('rollno')
            exam = request.form.get('exam')
            father = request.form.get('father')
            mother = request.form.get('mother')

            enter_student_info(sname,course,start_batch,end_batch,semester,enroll_no,
                            rollno,exam,father,mother)
            return redirect(url_for("info_hit", msg="success"))
        
    return render_template("forms/insert_student.html")
if __name__ =="__main__":
    app.run(debug=True)