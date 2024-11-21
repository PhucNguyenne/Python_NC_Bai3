from model import DbConn
import psycopg2
class StudentController:
    def __init__(self, treeview):
        self.treeview = treeview

    def load_all_students(self):
        # Sử dụng DbConn để lấy dữ liệu sinh viên từ database
        with DbConn() as db:
            results = db.select()  # Lấy tất cả sinh viên từ bảng
            # Xóa tất cả nội dung hiện tại trong Treeview
            self.treeview.delete(*self.treeview.get_children())
            # Chèn từng dòng kết quả vào Treeview
            for row in results:
                self.treeview.insert('', 'end', values=row)

    def insert_student(self, **student_data):
        with DbConn() as db:
            success = db.insert(**student_data)
            return success

    def update_student(self, update_data, **conditions):
        with DbConn() as db:
            success = db.update(update_data, **conditions)
            return success

    def delete_student(self, **conditions):
        with DbConn() as db:
            success = db.delete(**conditions)
            return success

# Thêm hàm này vào controller.py
def get_top_students():
    conn = psycopg2.connect(
        host="localhost",
        database="student_management",
        user="postgres",
        password="123456789"
    )
    cursor = conn.cursor()
    query = """
        SELECT mssv, fullname, class_name, birthday, python_score 
        FROM students 
        ORDER BY mssv 
        LIMIT 10;
    """
    cursor.execute(query)
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return students
