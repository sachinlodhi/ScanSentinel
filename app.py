from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
from predictor import predict

app = Flask(__name__)

UPLOAD_FOLDER = 'tmp'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyse_image', methods=['POST'])
def analyse_image():
    try:
        if 'file' not in request.files:
            return jsonify({'message': 'No file part', 'status': 'error'}), 400

        file = request.files['file']

        if file and allowed_file(file.filename):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            predicted_class, confidence, decoded_text = predict(file_path)

            response = {
                'message': 'Analysis completed',
                'filename': file.filename,
                'status': 'success',
                'file_path': f'/uploads/{file.filename}',
                'prediction': {
                    'class': predicted_class,
                    'confidence': confidence,
                    'decoded_text': decoded_text
                }
            }
            return jsonify(response), 201, {'Content-Type': 'application/json; charset=utf-8'}

        else:
            return jsonify({'message': 'Invalid file type', 'status': 'error'}), 400

    except Exception as e:
        return jsonify({'message': str(e), 'status': 'error'}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True)