# Sử dụng Python 3.11 làm base image
FROM python:3.11-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép file requirements.txt vào container
COPY requirements.txt .

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Expose cổng 5000 để truy cập Flask
EXPOSE 5000

# Thiết lập biến môi trường cho Flask
ENV FLASK_ENV=production

# Lệnh để chạy ứng dụng Flask
CMD ["python", "app.py"]
