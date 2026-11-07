import os
import pymysql
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def get_connection():
    """Create and return a secure TLS connection to TiDB Cloud."""
    return pymysql.connect(
        host=os.getenv("TIDB_HOST", "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"),
        port=int(os.getenv("TIDB_PORT", 4000)),
        user=os.getenv("TIDB_USER"),
        password=os.getenv("TIDB_PASSWORD"),
        database=os.getenv("TIDB_DATABASE", "sdsf_db"),
        ssl_verify_cert=False
    )

def create_table():
    """Ensure the studenttable exists in TiDB Cloud."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""-- sql
                create table if not exists studenttable (
                    id int auto_increment primary key,
                    enrollment_no varchar(64) unique,
                    name varchar(255),
                    course varchar(255),
                    start_batch varchar(32),
                    end_batch varchar(32),
                    sem varchar(32),
                    rollno varchar(64),
                    exam varchar(64),
                    father varchar(255),
                    mother varchar(255),
                    created_at timestamp default current_timestamp
                );
            """)
        connection.commit()
    finally:
        connection.close()

def checking_enroll_no(enroll_no):
    """Check if an enrollment number already exists in TiDB Cloud."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""-- sql
                select exists(
                    select 1 from studenttable where enrollment_no = '{enroll_no}'
                );
            """)
            result = cursor.fetchone()
            return result[0] == 1
    finally:
        connection.close()

def enter_student_info(name, course, start_batch, end_batch, semester, enroll_no,
                       rollno, exam, father, mother):
    """Insert a new student record into TiDB Cloud."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""-- sql
                insert into studenttable
                (enrollment_no, name, course, start_batch, end_batch, sem, rollno, exam, father, mother)
                values
                ('{enroll_no}', '{name}', '{course}', '{start_batch}', '{end_batch}', '{semester}', '{rollno}', '{exam}', '{father}', '{mother}');
            """)
        connection.commit()
    finally:
        connection.close()

def view_courses(enroll_no):
    """To view that particular course only as enroll_no is unique"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""-- sql
                select * from studenttable where enrollment_no = '{enroll_no}';
            """)
            result = cursor.fetchall()
            '''
            By default in Python, cursor.fetchall() returns a list of tuples, where each tuple represents one database row:
            eg:
            [
                (1, 'DE1234567', 'Joyobrata Das', 'ds', '2026', '2028', '1', 'DS7B-8978', '2026-11-01', 'Father Name', 'Mother Name', '2026-11-07 05:00:00')
            ]
            '''
            return result
    finally:
        connection.close()


def course_table(table_name):
    """To view the course details basically """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""-- sql
                select * from {table_name};
            """)
            result = cursor.fetchall()
           
            return result
    finally:
        connection.close()