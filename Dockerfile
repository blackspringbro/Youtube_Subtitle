FROM python:3.11-slim
WORKDIR /srv
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app

# Render は任意のPORTを割り当てる。EXPOSEは任意だが残しても可
# EXPOSE 8000

# $PORT を使って起動（PORTが未設定なら8000）
CMD bash -lc 'uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}'
