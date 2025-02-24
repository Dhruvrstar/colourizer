from flask import Flask, jsonify, send_file, render_template, request
from flask_cors import CORS
import cv2
import os
from datetime import datetime
from colorizer import colorize_image

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/colorize', methods=['POST'])
def api_colorize():
    try:
        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'error': 'No file uploaded'
            }), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'error': 'Empty filename'
            }), 400

        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        upload_path = os.path.join(UPLOAD_FOLDER, filename)
        output_path = os.path.join(OUTPUT_FOLDER, filename)
        
        file.save(upload_path)
        output_image = colorize_image(upload_path)
        cv2.imwrite(output_path, output_image)

        return jsonify({
            'status': 'success',
            'downloadUrl': f'/download/{filename}'
        })

    except Exception as e:
        app.logger.error(f'Error processing image: {str(e)}')
        return jsonify({
            'status': 'error',
            'error': 'Failed to process image. Please try again.'
        }), 500

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(
        os.path.join(OUTPUT_FOLDER, filename),
        mimetype='image/jpeg',
        as_attachment=True
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)