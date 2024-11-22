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
        query = sql.SQL("SELECT * FROM {table} WHERE username = %s AND password = %s").format(
            table=sql.Identifier("users")
        )
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()
        if result:
            return {'username': result[0], 'role': result[1]}
        return None

    def register_user(self, username, password):
        try:
            # Kiểm tra xem username đã tồn tại chưa
            query_check = sql.SQL("SELECT * FROM {table} WHERE username = %s").format(
                table=sql.Identifier("users")
            )
            self.cursor.execute(query_check, (username,))
            if self.cursor.fetchone() is not None:
                print(f"Username '{username}' already exists.")
                return False

            # Thêm người dùng mới
            query_insert = sql.SQL("INSERT INTO {table} (username, password) VALUES (%s, %s)").format(
                table=sql.Identifier("users")
            )
            self.cursor.execute(query_insert, (username, password))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error registering user: {e}")
            return False

    def insert(self, **kwargs):
        try:
            columns = kwargs.keys()
            values = kwargs.values()
            query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({placeholders})").format(
                table=sql.Identifier("students"),
                fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
                placeholders=sql.SQL(', ').join(sql.Placeholder() * len(columns))
            )
            self.cursor.execute(query, tuple(values))
            self.conn.commit()
            return True
        except Exception as ex:
            self.conn.rollback()
            print(f"Error inserting student: {ex}")
            return False

    def delete(self, **conditions):
        try:
            conds = [sql.SQL("{} = {}").format(sql.Identifier(k), sql.Placeholder()) for k in conditions.keys()]
            query = sql.SQL("DELETE FROM {table} WHERE {conds}").format(
                table=sql.Identifier("students"),
                conds=sql.SQL(" AND ").join(conds)
            )
            self.cursor.execute(query, tuple(conditions.values()))
            self.conn.commit()
            return True
        except Exception as ex:
            self.conn.rollback()
            print(f"Error deleting student: {ex}")
            return False

    def select(self, **conditions):
        try:
            conds = [sql.SQL("{} = {}").format(sql.Identifier(k), sql.Placeholder()) for k in conditions.keys()]
            query = sql.SQL("SELECT * FROM {table} WHERE {conds} ORDER BY mssv ASC").format(
                table=sql.Identifier("students"),
                conds=sql.SQL(" AND ").join(conds)
            )
            self.cursor.execute(query, tuple(conditions.values()))
            rows = self.cursor.fetchall()
            results = [
                {
                    'mssv': row[0],
                    'fullname': row[1],
                    'class_name': row[2],
                    'birthday': row[3],
                    'python_score': row[4]
                }
                for row in rows
            ]
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
            query = sql.SQL("SELECT * FROM {table} WHERE mssv = %s").format(
                table=sql.Identifier("students")
            )
            self.cursor.execute(query, (mssv,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error fetching student: {e}")
            return None
