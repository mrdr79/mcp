# Sử dụng Python 3.10 trên nền Linux nhẹ (Slim)
FROM python:3.10-slim

# Cập nhật và cài đặt FFmpeg + Git
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy các file code vào server
COPY . .

# Cài đặt thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# Mở lệnh chạy server
CMD ["python", "server.py"]
