from flask import Flask, render_template, request, jsonify
import numpy as np
from tensorflow import keras
from PIL import Image
import cv2
import os


app = Flask(__name__, static_folder='static')

current_dir = os.path.dirname(os.path.abspath(__file__))
h5_file_path = os.path.join(current_dir, "vgg16_model.h5")

# Load the model
model = keras.models.load_model(h5_file_path)

label=["Data Loss ","No ","Salt And Pepper ","Stripe "]
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Access the uploaded file
        if 'file' not in request.files:
            return {"result": "No image uploaded"}
        # Read and process the image data
        uploaded_file = request.files['file']
        image_data = uploaded_file.read()
        np_arr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        # Preprocess the image
        image = Image.fromarray(image)
        image = image.resize((224, 224))  # Adjust the size to match your model's input requirements
        image = np.array(image)
        image = image / 255.0  # Normalize the image pixel values (if required)
        image = np.expand_dims(image, axis=0)  # Add an extra dimension to match the model's input shape

        # Perform the prediction
        print(type(image))
        predictions = model.predict(image)

        # Interpret the results
        predicted_class = np.argmax(predictions, axis=1)
        print(f"Predicted class: {predicted_class}")

        res = {"result": f"{label[int(predicted_class)]} Noise Detected"}
        return jsonify(res)
    
    return render_template("index.html")

@app.route('/close_modal', methods=['POST'])
def close_modal():
    return ''

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)
