import os
import sqlite3
import random
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.preprocessing import image

app = Flask(__name__)

# Configure a temporary uploads folder for evaluation files
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# 1. AI MODEL INITIALIZATION & LOADING

MODEL_PATH = 'densenet121_ham10000.keras'

print("🔄 Loading DenseNet121 Skin Cancer Diagnostic Weights...")
try:
    
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    print("✅ AI Model successfully cached into system memory!")
except Exception as e:
    print(f" Critical Error: Could not locate or read {MODEL_PATH}.")
    print("Please verify the file name is correct and placed in the main directory.")
    print(str(e))


CLASSES = {
    0: 'Actinic keratoses (akiec) - Pre-Malignant',
    1: 'Basal cell carcinoma (bcc) - Malignant Carcinoma',
    2: 'Benign keratosis-like lesions (bkl) - Benign Mimicker',
    3: 'Dermatofibroma (df) - Benign Fibroma',
    4: 'Melanoma (mel) - Malignant Oncology Target',
    5: 'Melanocytic nevi (nv) - Benign Proliferation (Common Mole)',
    6: 'Vascular lesions (vasc) - Benign Vascular Proliferation'
}


# 2. DATABASE ROUTING HELPER FUNCTION

def get_randomized_kolkata_doctors():
    """Queries doctors.db and returns 4 random specialists to prevent UI clutter."""
    try:
        conn = sqlite3.connect('doctors.db')
        cursor = conn.cursor()
        
        # Pull all verified HexaHealth Kolkata entries
        cursor.execute("SELECT name, hospital, address, phone, specialization FROM doctors")
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return []
            
        all_doctors = [
            {
                "name": r[0],
                "hospital": r[1],
                "address": r[2],
                "phone": r[3],
                "specialization": r[4]
            }
            for r in rows
        ]
        
        # Return a randomized sample subset of 4 doctors maximum
        return random.sample(all_doctors, min(4, len(all_doctors)))
        
    except sqlite3.OperationalError:
        print("⚠️ Warning: doctors.db not found or uninitialized. Run init_db.py first!")
        return []
    except Exception as e:
        print(f"Database extraction error: {str(e)}")
        return []


# 3. CORE FLASK APPLICATION ROUTING


@app.route('/')
def home():
    """Serves your Single Page Application frontend dashboard."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Receives dermoscopic images, performs inference, and appends specialist cards."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file segment found in request payload'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for evaluation'}), 400

    try:
        
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        
        img = image.load_img(filepath, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        
        predictions = model.predict(img_array)[0]
        max_index = np.argmax(predictions)
        
        disease_profile = CLASSES[max_index]
        probability_score = float(predictions[max_index]) * 100

        # Clean up the file locally after evaluation to save space
        if os.path.exists(filepath):
            os.remove(filepath)

        
        response_payload = {
            'disease': disease_profile,
            'probability': f"{probability_score:.2f}%",
            'doctors': []
        }

        # If the condition falls under high-risk parameters, query and inject Kolkata doctors
        # This matches class index 0 (akiec), 1 (bcc), and 4 (mel)
        if max_index in [0, 1, 4]:
            response_payload['doctors'] = get_randomized_kolkata_doctors()

        return jsonify(response_payload)

    except Exception as e:
        print(f"🚨 Pipeline Exception triggered: {str(e)}")
        return jsonify({'error': f'Internal server exception during matrix evaluation: {str(e)}'}), 500


# 4. ENGINE STARTER

if __name__ == '__main__':
    # Starts your server at http://127.0.0.1:5000/
    app.run(host='127.0.0.1', port=5000, debug=True)
