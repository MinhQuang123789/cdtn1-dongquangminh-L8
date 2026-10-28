FROM python:3.12-slim
WORKDIR /app

# Chép tệp khoá TRƯỚC rồi cài - Docker cache lớp này
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Chép toàn bộ mã nguồn
COPY . .

# Lệnh mặc định
CMD ["python", "-m", "src.pipeline"]