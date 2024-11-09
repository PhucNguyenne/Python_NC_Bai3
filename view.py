import tkinter as tk
from tkinter import ttk, messagebox
import controller
from tkinter import filedialog


class LoginView:
    def __init__(self, master, on_login_success):
        self.master = master
        self.on_login_success = on_login_success
        self.setup_login_view()
        self.master.title("Đăng nhập")
    def setup_login_view(self):
        self.master.geometry("250x200")
        tk.Label(self.master, text="Tên người dùng:").pack(pady=5)
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack(pady=5)

        tk.Label(self.master, text="Mật khẩu:").pack(pady=5)
        self.password_entry = tk.Entry(self.master, show='*')
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.master, text="Đăng nhập", command=self.login)
        self.login_button.pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        with controller.DbConn() as db:
            if db.check_login(username, password):
                self.on_login_success()  # Gọi hàm khi đăng nhập thành công
            else:
                messagebox.showerror("Lỗi", "Tên người dùng hoặc mật khẩu không đúng.")


class StudentManagementApp:
    def __init__(self, root, logout_callback):
        self.root = root
        self.logout_callback = logout_callback
        self.root.title("Quản lý sinh viên")
        self.root.geometry("")
        # Tạo thanh menu
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Thêm mục "File"
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Thoát", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Thêm mục "Tài khoản"
        account_menu = tk.Menu(self.menu_bar, tearoff=0)
        account_menu.add_command(label="Đăng xuất", command=self.logout_callback)
        self.menu_bar.add_cascade(label="Tài khoản", menu=account_menu)

        # Tạo Notebook để chứa các tab
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True)

        # Thêm các tab
        self.add_tab = ttk.Frame(self.notebook)
        self.edit_tab = ttk.Frame(self.notebook)
        self.delete_tab = ttk.Frame(self.notebook)
        self.search_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.add_tab, text="Thêm sinh viên")
        self.notebook.add(self.edit_tab, text="Sửa sinh viên")
        self.notebook.add(self.delete_tab, text="Xóa sinh viên")
        self.notebook.add(self.search_tab, text="Tìm kiếm sinh viên")
        
        self.setup_add_tab()
        self.setup_edit_tab()
        self.setup_delete_tab()
        self.setup_search_tab()
        
    def create_treeview(self, parent, columns):
        # Tạo Treeview để hiển thị kết quả
        treeview = ttk.Treeview(parent, columns=columns, show="headings", height=10)

        # Đặt tên cho các cột
        for col in columns:
            treeview.heading(col, text=col)

        treeview.grid(row=2, column=0, columnspan=2, sticky="nsew")

        # Thêm Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=treeview.yview)
        scrollbar.grid(row=2, column=2, sticky="ns")
        treeview.configure(yscrollcommand=scrollbar.set)

        # Đặt grid cho các hàng và cột
        parent.grid_rowconfigure(2, weight=1)
        parent.grid_columnconfigure(1, weight=1)

        return treeview


    def setup_add_tab(self):
        tk.Label(self.add_tab, text="Thông tin sinh viên").grid(row=0, column=0)

        columns = ("MSSV", "Họ tên", "Lớp", "Ngày sinh", "Điểm Python")
        self.add_tree = self.create_treeview(self.add_tab, columns)
        self.add_tree.grid(column=0, row=7)

        self.load_all_students_to_add_tree()  # Chỉ cập nhật cho add_tree

        tk.Label(self.add_tab, text="MSSV:").grid(row=1, column=0)
        tk.Label(self.add_tab, text="Họ tên:").grid(row=2, column=0)
        tk.Label(self.add_tab, text="Lớp:").grid(row=3, column=0)
        tk.Label(self.add_tab, text="Ngày sinh:").grid(row=4, column=0)
        tk.Label(self.add_tab, text="Điểm Python:").grid(row=5, column=0)

        self.mssv_entry = tk.Entry(self.add_tab)
        self.name_entry = tk.Entry(self.add_tab)
        self.class_entry = tk.Entry(self.add_tab)
        self.birthday_entry = tk.Entry(self.add_tab)
        self.python_score_entry = tk.Entry(self.add_tab)

        self.mssv_entry.grid(row=1, column=1)
        self.name_entry.grid(row=2, column=1)
        self.class_entry.grid(row=3, column=1)
        self.birthday_entry.grid(row=4, column=1)
        self.python_score_entry.grid(row=5, column=1)

        self.add_button = tk.Button(self.add_tab, text="Thêm sinh viên", command=self.add_student)
        self.add_button.grid(row=6, columnspan=2, padx=10, pady=5)
        
        self.reset_button = tk.Button(self.add_tab, text="Reset", command=self.load_all_students_to_add_tree)
        self.reset_button.grid(row=6, columnspan=2, padx=10, pady=5, sticky="w")

    def setup_edit_tab(self):
        tk.Label(self.edit_tab, text="MSSV:").grid(row=0, column=0)
        self.edit_mssv_entry = tk.Entry(self.edit_tab)
        self.edit_mssv_entry.grid(row=0, column=1)

        columns = ("MSSV", "Họ tên", "Lớp", "Ngày sinh", "Điểm Python")
        self.edit_tree = self.create_treeview(self.edit_tab, columns)  # Sử dụng edit_tree thay vì add_tree
        self.edit_tree.grid(column=0, row=9)

        self.load_all_students_to_edit_tree()  # Chỉ cập nhật cho edit_tree

        self.check_button = tk.Button(self.edit_tab, text="Kiểm tra", command=self.check_student)
        self.check_button.grid(row=5, columnspan=2, padx=5, pady=5)

        tk.Label(self.edit_tab, text="Họ tên:").grid(row=1, column=0)
        tk.Label(self.edit_tab, text="Lớp:").grid(row=2, column=0)
        tk.Label(self.edit_tab, text="Ngày sinh:").grid(row=3, column=0)
        tk.Label(self.edit_tab, text="Điểm Python:").grid(row=4, column=0)

        self.edit_name_entry = tk.Entry(self.edit_tab, state='readonly')
        self.edit_class_entry = tk.Entry(self.edit_tab, state='readonly')
        self.edit_birthday_entry = tk.Entry(self.edit_tab, state='readonly')
        self.edit_python_score_entry = tk.Entry(self.edit_tab, state='readonly')

        self.edit_name_entry.grid(row=1, column=1)
        self.edit_class_entry.grid(row=2, column=1)
        self.edit_birthday_entry.grid(row=3, column=1)
        self.edit_python_score_entry.grid(row=4, column=1)

        self.update_button = tk.Button(self.edit_tab, text="Cập nhật", command=self.update_student)
        self.update_button.grid(row=6, columnspan=2, padx=5, pady=5)
        
        self.reset_button = tk.Button(self.edit_tab, text="Reset", command=self.load_all_students_to_edit_tree)
        self.reset_button.grid(row=7, columnspan=2, padx=10, pady=5, sticky="w")

    def setup_delete_tab(self):
        tk.Label(self.delete_tab, text="MSSV:").grid(row=0, column=0)
        self.delete_mssv_entry = tk.Entry(self.delete_tab)
        self.delete_mssv_entry.grid(row=0, column=1)

        columns = ("MSSV", "Họ tên", "Lớp", "Ngày sinh", "Điểm Python")
        self.delete_tree = self.create_treeview(self.delete_tab, columns)  # Sử dụng delete_tree thay vì add_tree
        self.delete_tree.grid(column=0, row=3)

        self.load_all_students_to_delete_tree()  # Chỉ cập nhật cho delete_tree

        self.delete_button = tk.Button(self.delete_tab, text="Xóa sinh viên", command=self.delete_student)
        self.delete_button.grid(row=1, columnspan=2)
        
        self.reset_button = tk.Button(self.delete_tab, text="Reset", command=self.load_all_students_to_delete_tree)
        self.reset_button.grid(row=2, columnspan=2, padx=10, pady=5, sticky="w")

    def load_all_students_to_add_tree(self):
        with controller.DbConn() as db:
            results = db.select()
            self.add_tree.delete(*self.add_tree.get_children())
            for row in results:
                self.add_tree.insert('', 'end', values=row)

    def load_all_students_to_edit_tree(self):
        with controller.DbConn() as db:
            results = db.select()
            self.edit_tree.delete(*self.edit_tree.get_children())
            for row in results:
                self.edit_tree.insert('', 'end', values=row)

    def load_all_students_to_delete_tree(self):
        with controller.DbConn() as db:
            results = db.select()
            self.delete_tree.delete(*self.delete_tree.get_children())
            for row in results:
                self.delete_tree.insert('', 'end', values=row)

    
    def add_student(self):
        mssv = self.mssv_entry.get()
        fullname = self.name_entry.get()
        class_name = self.class_entry.get()
        birthday = self.birthday_entry.get()
        python_score = self.python_score_entry.get()

        with controller.DbConn() as db:
            if db.insert(mssv=mssv, fullname=fullname, class_name=class_name, birthday=birthday, python_score=python_score):
                messagebox.showinfo("Thành công", "Sinh viên đã được thêm thành công.")
                self.load_all_students_to_add_tree()
            else:
                messagebox.showerror("Lỗi", "Sinh viên với MSSV đã tồn tại.")
    
    def check_student(self):
        mssv = self.edit_mssv_entry.get()
        with controller.DbConn() as db:
            student = db.select(mssv=mssv)
            if student:
                self.edit_name_entry.config(state='normal')
                self.edit_class_entry.config(state='normal')
                self.edit_birthday_entry.config(state='normal')
                self.edit_python_score_entry.config(state='normal')

                self.edit_name_entry.delete(0, tk.END)
                self.edit_name_entry.insert(0, student[0][1])  # Họ tên
                self.edit_class_entry.delete(0, tk.END)
                self.edit_class_entry.insert(0, student[0][2])  # Lớp
                self.edit_birthday_entry.delete(0, tk.END)
                self.edit_birthday_entry.insert(0, student[0][3])  # Ngày sinh
                self.edit_python_score_entry.delete(0, tk.END)
                self.edit_python_score_entry.insert(0, student[0][4])  # Điểm Python
            else:
                messagebox.showerror("Lỗi", "Sinh viên không tồn tại.")

    def update_student(self):
        mssv = self.edit_mssv_entry.get()
        update_data = {
            'fullname': self.edit_name_entry.get(),
            'class_name': self.edit_class_entry.get(),
            'birthday': self.edit_birthday_entry.get(),
            'python_score': self.edit_python_score_entry.get(),
        }

        with controller.DbConn() as db:
            if db.update(update_data, mssv=mssv):
                messagebox.showinfo("Thành công", "Thông tin sinh viên đã được cập nhật.")
                # self.load_all_students()
            else:
                messagebox.showerror("Lỗi", "Cập nhật không thành công.")


    def delete_student(self):
        mssv = self.delete_mssv_entry.get()

        with controller.DbConn() as db:
            if db.delete(mssv=mssv):
                messagebox.showinfo("Thành công", "Sinh viên đã được xóa thành công.")
                # self.load_all_students()
            else:
                messagebox.showerror("Lỗi", "Sinh viên không tồn tại.")

    def setup_search_tab(self):
        tk.Label(self.search_tab, text="Tìm kiếm theo MSSV:").grid(row=0, column=0)
        self.search_mssv_entry = tk.Entry(self.search_tab)
        self.search_mssv_entry.grid(row=0, column=1)

        self.search_button = tk.Button(self.search_tab, text="Tìm kiếm", command=self.search_student)
        self.search_button.grid(row=1, column=1)  # Đưa nút tìm kiếm về cột 0

        # Nút lưu kết quả tìm kiếm
        self.save_button = tk.Button(self.search_tab, text="Lưu kết quả", command=self.save_results_to_file)
        self.save_button.grid(row=3, column=1)  # Đặt nút lưu ở cột 1 cùng hàng với nút tìm kiếm

        # Sử dụng hàm tiện ích để tạo Treeview và Scrollbar
        columns = ("MSSV", "Họ tên", "Lớp", "Ngày sinh", "Điểm Python")
        self.results_tree = self.create_treeview(self.search_tab, columns)
        self.results_tree.grid(column=0, row=2, columnspan=2)  # Điều chỉnh vị trí cho Treeview
        

    def search_student(self):
        mssv = self.search_mssv_entry.get()
        
        # Kết nối với database và tìm kiếm sinh viên theo MSSV
        with controller.DbConn() as db:
            results = db.select(mssv=mssv)
            
            # Xóa tất cả nội dung cũ trong Treeview trước khi hiển thị kết quả mới
            self.results_tree.delete(*self.results_tree.get_children())  # Xóa tất cả các hàng
            
            # Kiểm tra và hiển thị kết quả tìm kiếm
            if results:
                for row in results:
                    self.results_tree.insert('', 'end', values=row)  # Thêm từng kết quả vào Treeview
       
            else:
                messagebox.showinfo("Thông báo", "Không tìm thấy sinh viên.")  # Thông báo nếu không tìm thấy

    def check_student(self):
        mssv = self.edit_mssv_entry.get()
        with controller.DbConn() as db:
            student = db.select(mssv=mssv)
            if student:
                self.edit_name_entry.config(state='normal')
                self.edit_class_entry.config(state='normal')
                self.edit_birthday_entry.config(state='normal')
                self.edit_python_score_entry.config(state='normal')

                # Xóa nội dung cũ trong các Entry trước khi hiển thị thông tin mới
                self.edit_name_entry.delete(0, tk.END)
                self.edit_class_entry.delete(0, tk.END)
                self.edit_birthday_entry.delete(0, tk.END)
                self.edit_python_score_entry.delete(0, tk.END)

                # Điền thông tin sinh viên vào các trường
                self.edit_name_entry.insert(0, student[0][1])  # Họ tên
                self.edit_class_entry.insert(0, student[0][2])  # Lớp
                self.edit_birthday_entry.insert(0, student[0][3])  # Ngày sinh
                self.edit_python_score_entry.insert(0, student[0][4])  # Điểm Python
            else:
                messagebox.showerror("Lỗi", "Sinh viên không tồn tại.")


    def save_results_to_file(self):
    # Mở hộp thoại để chọn vị trí và tên file
        file_name = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                                                title="Lưu kết quả tìm kiếm")
        if file_name:  # Kiểm tra nếu người dùng không hủy bỏ
            try:
                with open(file_name, 'w') as f:
                    # Giả sử bạn có một list kết quả rows từ tìm kiếm trước đó
                    for row in self.results_tree.get_children():
                        row_values = self.results_tree.item(row, 'values')
                        f.write(', '.join(row_values) + '\n')
                print(f"Kết quả tìm kiếm đã được lưu vào {file_name}")
            except Exception as ex:
                print(f"Lỗi khi lưu file: {ex}")





