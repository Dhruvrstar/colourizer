from utils.helpers import (
    validate_image_file,
    generate_unique_filename,
    cleanup_temp_files,
    format_error_response
)

@app.route('/api/colorize', methods=['POST'])
def handle_request():
    try:
        if 'file' not in request.files:
            return format_error_response("No file uploaded", 400)
            
        file = request.files['file']
        validate_image_file(file)
        
        # Generate unique filename
        filename = generate_unique_filename(file.filename)
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            upload_path = os.path.join(tmp_dir, filename)
            file.save(upload_path)
            
            # Process image
            output_image = colorize_image(upload_path)
            
            # Save output
            output_path = os.path.join(tmp_dir, f"colorized_{filename}")
            cv2.imwrite(output_path, output_image)
            
            return send_file(output_path, mimetype='image/jpeg')

    except ValueError as e:
        return format_error_response(str(e), 400)
    except Exception as e:
        logging.error(f"Processing error: {str(e)}")
        return format_error_response("Internal server error", 500)
    finally:
        cleanup_temp_files(upload_path, output_path)