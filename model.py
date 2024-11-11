import psycopg2
from psycopg2 import sql

class DbConn:
    def __init__(self, connection=None, database="student_management", user="postgres", password="123456789", host="localhost", port="5432"):
        # Nếu đã có kết nối, sử dụng kết nối đó, nếu không tạo kết nối mới
        if connection:
            self.conn = connection
        else:
            self.conn = psycopg2.connect(
                database=database,
                user=user,
                password=password,
                host=host,
                port=port
            )
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.conn.close()

    def check_login(self, username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        return self.cursor.fetchone() is not None

    def insert(self, **kwargs):
        try:
            query = sql.SQL("INSERT INTO students (mssv, fullname, class_name, birthday, python_score) VALUES (%s, %s, %s, %s, %s)")
            self.cursor.execute(query, tuple(kwargs.values()))
            self.conn.commit()
            return True
        except Exception as ex:
            self.conn.rollback()
            print(f"Error inserting student: {ex}")
            return False

    def delete(self, **conditions):
        try:
            query = "DELETE FROM students WHERE mssv = %s"
            self.cursor.execute(query, (conditions['mssv'],))
            self.conn.commit()
            return True
        except Exception as ex:
            self.conn.rollback()
            print(f"Error deleting student: {ex}")
            return False

    def select(self, **conditions):
        try:
            query = "SELECT mssv, fullname, class_name, birthday, python_score FROM students WHERE mssv = %s"
            self.cursor.execute(query, (conditions['mssv'],))
            rows = self.cursor.fetchall()
            # Chuyển kết quả thành danh sách các dictionary
            results = []
            for row in rows:
                student = {
                    'mssv': row[0],
                    'fullname': row[1],
                    'class_name': row[2],
                    'birthday': row[3],
                    'python_score': row[4]
                }
                results.append(student)
            return results
        except Exception as e:
            print("Error fetching student:", e)
            return []

    def update_student(self, mssv, fullname, class_name, birthday, python_score):
        try:
            sql = """
            UPDATE students
            SET fullname = %s, class_name = %s, birthday = %s, python_score = %s
            WHERE mssv = %s
            """
            self.cursor.execute(sql, (fullname, class_name, birthday, python_score, mssv))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating student: {e}")
            self.conn.rollback()
            return False
    
    def get_student_by_mssv(self, mssv):
        try:
            sql = "SELECT * FROM students WHERE mssv = %s"
            self.cursor.execute(sql, (mssv,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error fetching student: {e}")
            return None
