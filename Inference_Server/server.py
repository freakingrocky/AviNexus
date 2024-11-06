import base64
import io

import numpy as np
import torch
from flask import Flask, jsonify, request
from flask_cors import CORS
from PIL import Image

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set the device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load YOLOv7 model directly onto the device
model = torch.load('init.pt', map_location=device)  # Load to appropriate device (GPU if available)
model = model.to(device)
model.eval()  # Set the model to evaluation mode
LABELS = ['bottles', 'cans', 'cardboard', 'clothes', 'detergent', 'glass', 'metal', 'paper', 'plastic', 'recyclable', 'organic-recyclable', 'biological', 'non-recyclable', 'shoes', 'teabags', 'battery', 'trash']

@app.route('/api/detect', methods=['POST'])
def detect():
    data = request.get_json()
    if 'image' in data:
        # Remove any prefix in the base64 data
        image_data = base64.b64decode(data['image'].split(',')[1] if ',' in data['image'] else data['image'])
        try:
            image = Image.open(io.BytesIO(image_data)).convert('RGB')
        except Exception as e:
            print("Image load error:", e)  # Debugging information
            return jsonify({"error": "Could not decode image"}), 400

        # Preprocess the image to fit YOLOv7 input format
        image_resized = image.resize((640, 640))  # YOLOv7 commonly uses 640x640
        image_array = np.array(image_resized) / 255.0  # Normalize to [0, 1] range
        image_tensor = torch.tensor(image_array).permute(2, 0, 1).unsqueeze(0).to(device).float()  # Convert to FloatTensor and move to device

        # Run the model on the image
        with torch.no_grad():
            predictions = model(image_tensor)[0]  # Get predictions

        # Debugging: print the structure of predictions for clarity
        print("Prediction structure:", predictions.shape)

        # Parse predictions, assuming each row corresponds to a bounding box prediction
        output = []
        for pred in predictions[0]:  # Iterate through each prediction in the first batch dimension
            # Extract bounding box coordinates, confidence, and label index
            bbox = [float(pred[0]), float(pred[1]), float(pred[2]), float(pred[3])]
            confidence = float(pred[4])
            label_idx = int(pred[5])
            label = LABELS[label_idx] if 0 <= label_idx < len(LABELS) else 'unknown'
            if confidence > 0.7:
                output.append({
                    "label": label,
                    "bbox": bbox,
                    "conf": confidence
                })

        return jsonify(output)
    else:
        return jsonify({"error": "No image data provided"}), 400

if __name__ == '__main__':
    app.run(port=8888)
