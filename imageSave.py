#from flask import Flask, request, jsonify
from flask import Blueprint, request, jsonify
from google.cloud import storage
import os
from datetime import datetime

#app = Flask(__name__)
image_save_blueprint = Blueprint('image_save', __name__)
# Konfigurasi credential dan nama bucket
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'config/cc-c241-ps246-60ba32f0ad56.json'
bucket_name = 'cc-c241-ps246.appspot.com'

# Inisialisasi Google Cloud Storage client
storage_client = storage.Client()

#@app.route('/upload', methods=['POST'])
@image_save_blueprint.route('/upload', methods=['POST'])
def upload_file():
    """Endpoint untuk mengunggah file ke Google Cloud Storage."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Menggunakan timestamp untuk membuat nama file unik
    current_time = datetime.utcnow().strftime('%Y-%m-%d-%H%M%S')
    filename = f"images-OCR/image-{current_time}.jpg"

    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)

        # Mengunggah file dengan nama baru
        blob.upload_from_string(
            file.read(),
            content_type=file.content_type
        )

        # Mengembalikan URL publik dari file yang diunggah
        url = blob.public_url
        return jsonify({'message': 'File successfully uploaded', 'url': url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#if __name__ == '__main__':
    #app.run(debug=True, port=5000)
