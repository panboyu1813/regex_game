FROM python:3.11-slim

# 環境變數（可根據需求在 docker run 時透過 -e 傳入或寫死在這裡）
ENV AUTO_UPDATE=0 \
    USE_UV=0 \
    ROOT_DIR="" \
    PY_FILE=main.py \
    REQUIREMENTS_FILE=requirements.txt \
    PY_PACKAGES=""

# 安裝必要工具
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

# 建立工作目錄
WORKDIR /home/container

# 複製所有檔案進容器
COPY . .

# 如果有 .git 且 AUTO_UPDATE = 1 就執行 git pull
RUN if [ -d .git ] && [ "$AUTO_UPDATE" = "1" ]; then git pull; fi

# 切換目錄
WORKDIR /home/container/${ROOT_DIR}

# 安裝 uv（如果有指定 USE_UV=1）
RUN if [ "$USE_UV" = "1" ]; then \
        if ! command -v uv > /dev/null && [ ! -f /root/.local/bin/uv ]; then \
            echo "Installing uv..." && \
            curl -LsSf https://astral.sh/uv/install.sh | sh; \
        fi; \
    fi

# 安裝 Python 套件（用 uv 或 pip）
RUN if [ "$USE_UV" = "1" ]; then \
        UV_CMD="/root/.local/bin/uv"; \
        if [ ! -z "$PY_PACKAGES" ]; then $UV_CMD pip install $PY_PACKAGES; fi; \
        if [ -f "${REQUIREMENTS_FILE}" ]; then $UV_CMD pip install -r ${REQUIREMENTS_FILE}; fi; \
    else \
        if [ ! -z "$PY_PACKAGES" ]; then pip install -U $PY_PACKAGES; fi; \
        if [ -f "${REQUIREMENTS_FILE}" ]; then pip install -U -r ${REQUIREMENTS_FILE}; fi; \
    fi

# 預設執行指令（根據 USE_UV）
CMD if [ "$USE_UV" = "1" ]; then \
        UV_CMD="/root/.local/bin/uv"; \
        if [ -f "pyproject.toml" ]; then \
            exec $UV_CMD run ${PY_FILE}; \
        else \
            $UV_CMD pip install --system $PY_PACKAGES 2>/dev/null; \
            $UV_CMD pip install --system -r ${REQUIREMENTS_FILE} 2>/dev/null; \
            exec python ${PY_FILE}; \
        fi; \
    else \
        exec python ${PY_FILE}; \
    fi
