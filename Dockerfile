FROM python:3.11-slim

# 安裝必要工具
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

# 建立工作目錄
WORKDIR /home/container

# 複製所有檔案進容器
COPY . .

# 安裝 Python 套件
RUN pip install --no-cache-dir flask requests python-dotenv

# 設定 Flask app 名稱（對應 app.py 中的 app）
ENV FLASK_APP=app.py

# 開放 Flask port
EXPOSE 30003

# 執行 Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=30003"]
