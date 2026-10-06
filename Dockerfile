# Gunakan OS Linux versi ringan yang sudah terinstal Python
FROM python:3.9-slim

# Bikin folder khusus untuk aplikasi di dalam server
WORKDIR /app

# Copy file requirements dan install library-nya
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy file utama main.py
COPY main.py .

# Jalankan server FastAPI di port 7860 (Syarat wajib dari Hugging Face)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]