# 使用官方 Python 映像
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 複製專案檔案
COPY . /app

# 安裝 Flask
RUN pip install flask

# 開啟 port
EXPOSE 5000

# 啟動 Flask 應用
CMD ["python", "app.py"]

