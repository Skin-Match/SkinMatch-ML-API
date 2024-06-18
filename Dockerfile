# Gunakan image resmi Python sebagai base image
FROM python:3.8-slim

# Set working directory di dalam container
WORKDIR /app

# Copy file requirements.txt ke dalam container (pastikan Anda sudah membuatnya)
COPY requirements.txt .

# Install libraries Python yang diperlukan
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file sumber dari direktori lokal ke dalam container
COPY . .

# Expose port yang akan digunakan Flask (default: 5000)
EXPOSE 5000

# Command untuk menjalankan aplikasi saat container di-start
CMD ["python", "app.py"]
