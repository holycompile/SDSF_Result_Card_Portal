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
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS studenttable (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    enrollment_no VARCHAR(64) UNIQUE,
                    name VARCHAR(255),
                    course VARCHAR(255),
                    start_batch VARCHAR(32),
                    end_batch VARCHAR(32),
                    sem VARCHAR(32),
                    rollno VARCHAR(64),
                    exam VARCHAR(64),
                    father VARCHAR(255),
                    mother VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
            cursor.execute(
                "SELECT EXISTS(SELECT 1 FROM studenttable WHERE enrollment_no = %s);",
                (enroll_no,)
            )
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
            cursor.execute("""
                INSERT INTO studenttable
                (enrollment_no, name, course, start_batch, end_batch, sem, rollno, exam, father, mother)
                VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (enroll_no, name, course, start_batch, end_batch, semester, rollno, exam, father, mother))
        connection.commit()
    finally:
        connection.close()
