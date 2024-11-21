from flask import Flask, render_template, request, redirect, url_for, flash, session
from model import DbConn
from functools import wraps

app = Flask(__name__)
app.secret_key = "pn"

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('Bạn không có quyền truy cập vào trang này.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Vui lòng đăng nhập trước.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
# Trang đăng nhập
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with DbConn() as db:
            user_info = db.check_login(username, password)
            if user_info:
                role = user_info['role']
                session['username'] = username
                session['role'] = role
                return redirect(url_for('dashboard'))
            else:
                flash("Sai tên đăng nhập hoặc mật khẩu")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Sử dụng lớp DbConn để đăng ký người dùng
        with DbConn() as db:
            if db.register_user(username, password):
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Username already exists. Please try another one.', 'danger')

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Đã đăng xuất thành công.', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    from controller import get_top_students
    students = get_top_students()
    return render_template('dashboard.html', students=students)

# Thêm sinh viên
@app.route('/add', methods=['GET', 'POST'])
@admin_required
def add_student():
    if request.method == 'POST':
        data = {
            'mssv': request.form['mssv'],
            'fullname': request.form['fullname'],
            'class_name': request.form['class_name'],
            'birthday': request.form['birthday'],
            'python_score': request.form['python_score']
        }
        with DbConn() as db:
            if db.insert(**data):
                flash("Thêm sinh viên thành công")
            else:
                flash("Sinh viên đã tồn tại")
        return redirect(url_for('dashboard'))
    return render_template('add_student.html')

# Xóa sinh viên
@app.route('/delete_student', methods=['GET', 'POST'])
@admin_required
def delete_student():
    if request.method == 'POST':
        student_id = request.form['student_id']
        with DbConn() as db:
            if db.delete(mssv=student_id):
                flash("Xóa sinh viên thành công")
            else:
                flash("Sinh viên không tồn tại")
        return redirect(url_for('dashboard'))
    return render_template('delete_student.html')

# Tìm kiếm sinh viên
@app.route('/search', methods=['GET', 'POST'])

def search_student():
    results = []
    if request.method == 'POST':
        keyword = request.form['keyword']
        with DbConn() as db:
            results = db.select(mssv=keyword)
    return render_template('search_student.html', results=results)

# Sửa sinh viên
@app.route('/edit_student', methods=['GET', 'POST'])
def edit_student():
    student = None
    if request.method == 'POST' and 'search' in request.form:
        # Lấy MSSV người dùng nhập vào
        mssv = request.form['mssv']
        
        # Tìm sinh viên từ cơ sở dữ liệu
        with DbConn() as db:
            student = db.select(mssv=mssv)  # Giả sử bạn có phương thức select để tìm sinh viên
            if student:
                student = student[0]  # Chỉ lấy sinh viên đầu tiên
            else:
                flash("Sinh viên không tồn tại")
                return redirect(url_for('edit_student'))  # Quay lại trang sửa nếu không tìm thấy sinh viên
    
    elif request.method == 'POST' and 'update' in request.form:
        # Khi người dùng gửi thông tin cập nhật
        mssv = request.form['mssv']
        fullname = request.form['fullname']
        class_name = request.form['class_name']
        birthday = request.form['birthday']
        python_score = request.form['python_score']
        
        # Cập nhật thông tin sinh viên trong cơ sở dữ liệu
        with DbConn() as db:
            # Sử dụng phương thức update_student của DbConn để cập nhật thông tin
            if db.update_student(mssv, fullname, class_name, birthday, python_score):
                flash("Cập nhật sinh viên thành công")
                return redirect(url_for('dashboard'))  # Quay lại dashboard sau khi thành công
            else:
                flash("Lỗi cập nhật sinh viên")
                return redirect(url_for('edit_student'))  # Quay lại trang sửa nếu có lỗi

    return render_template('edit_student.html', student=student)

@app.route('/update_student', methods=['GET', 'POST'])
def update_student():
    student = None

    if request.method == 'POST':
        mssv = request.form.get('mssv')
        
        # Tìm kiếm sinh viên theo MSSV
        if mssv:
            with DbConn() as db:
                student_data = db.get_student_by_mssv(mssv)
                if student_data:
                    student = {
                        'mssv': student_data[0],
                        'fullname': student_data[1],
                        'class_name': student_data[2],
                        'birthday': student_data[3],
                        'python_score': student_data[4]
                    }
    
    # Render lại trang với thông tin sinh viên nếu tìm thấy
    return render_template('update_student.html', student=student)

if __name__ == '__main__':
    app.run(debug=True)
