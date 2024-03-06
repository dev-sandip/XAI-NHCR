import io
import time
import cv2
from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
from PIL import Image  # For image processing (optional)
import os
import base64
import json
from .model import predict

ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key='your_secret_key'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/about')
def aboutus():
    return render_template('about.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    
    
    if 'file-input' in request.files:
        uploaded_file = request.files['file-input']
        
        
        if uploaded_file and allowed_file(uploaded_file.filename):
        
            filename= uploaded_file.filename
            
            try:
                # Read and validate the image (modify as needed)
                image_buffer=io.BytesIO(uploaded_file.read()) 
                
                # print(image_buffer.getvalue())
                
                pred= predict(image_buffer=image_buffer)
                    
            
                return jsonify(pred)

            except (IOError, OSError, ValueError) as e:
                return jsonify(json.dumps({'error': "Server Error "+ str(e)})), 500
                

        else:
            return jsonify(json.dumps({'error': "Invalid file format. Please upload a  JPEG, or JPG image."})), 500
            
        
    if 'file-input-64'  in request.form:
        try:
    # Decode the base64 data (replace with your processing logic)
            base64_data = request.form['file-input-64']
            
            image_buffer= io.BytesIO(base64.b64decode(base64_data))
            
            
            try: 
                image_buffer.seek(0)

    # Use Pillow to open the image data from BytesIO
                image = Image.open(image_buffer)

    # Save the image as a JPEG with appropriate quality (adjust quality as needed)
                # image.save("canvas.jpeg", quality=90, format="JPEG")                
                image_buffer.seek(0)
                
                pred= predict(image_buffer=image_buffer)
                return jsonify(pred)

            except (IOError, OSError, ValueError) as e:
                return jsonify(json.dumps({'error': "Khali Na Patha"})), 500
                
            
            
        except Exception as e:
            return jsonify(json.dumps({'error': str(e)})), 500

if __name__ == '__main__':
    app.run(debug=True,reload=True)
