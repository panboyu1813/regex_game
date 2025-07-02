FROM python:3.9

# 換台灣鏡像源加快速度（可選）
RUN sed -i 's/deb.debian.org/mirror.twds.com.tw/g' /etc/apt/sources.list.d/debian.sources || true
RUN sed -i 's/security.debian.org/mirror.twds.com.tw/g' /etc/apt/sources.list.d/debian.sources || true

# 更新 pip 並只安裝 flask（不裝 pycryptodome 或 chromium）
RUN pip3 install --upgrade pip
RUN pip3 install flask

# 工作目錄與檔案
WORKDIR /app
COPY . /app
RUN rm /app/Dockerfile

# 設定環境變數讓 flask run 可執行
ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=5000

# 開放 port
EXPOSE 5000

# 執行 flask
ENTRYPOINT [ "flask" ]
CMD ["run", "--host=0.0.0.0"]
