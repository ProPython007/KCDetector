from skimage.metrics import structural_similarity as ssim
from flask import Flask, request, jsonify
from keras.models import load_model
import numpy as np
import joblib
import cv2
import os

app = Flask(__name__)

# Constants
IM_SIZE = 512

# Load the saved feature extractor model:
feature_extractor = load_model('static/assets/feature_extractor_model.h5')

# Load the saved Random Forest model:
RF_model = joblib.load('static/assets/RF_model.pkl')
# RF_model = joblib.load('static/assets/RF_model2.pkl')

# Load the saved LabelEncoder:
le = joblib.load('static/assets/label_encoder.pkl')


# Utility function to process the image directly from bytes:
def process_img(img_bytes):
    # Convert bytes data to numpy array
    npimg = np.frombuffer(img_bytes, np.uint8)
    
    # Decode image
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply binary thresholding
    _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find the largest contour and get bounding box
    max_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(max_contour)
    
    # Crop the image based on the bounding box
    cropped_image = image[y:y+h, x:x+w]
    
    return cropped_image


def resize_to_smallest(image1, image2):
    # Get dimensions of both images
    h1, w1 = image1.shape[:2]
    h2, w2 = image2.shape[:2]
    
    # Determine the smallest dimensions
    new_height = min(h1, h2)
    new_width = min(w1, w2)
    
    # Resize both images to the smallest dimensions
    resized_image1 = cv2.resize(image1, (new_width, new_height))
    resized_image2 = cv2.resize(image2, (new_width, new_height))
    
    return resized_image1, resized_image2


# API route for prediction:
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get image file from the request
        ufile = request.files['image']
        
        # Read the image directly from the uploaded file into bytes
        img_bytes = ufile.read()
        
        # Process the image
        img_obj = process_img(img_bytes)
        img = cv2.resize(img_obj, (IM_SIZE, IM_SIZE))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        
        # Extract features using the feature extractor
        X_test_feature = feature_extractor.predict(np.array([img]))
        
        # Perform prediction using the Random Forest model
        prediction_RF = RF_model.predict(X_test_feature)
        prediction_RF = le.inverse_transform(prediction_RF)
        
        # Encode the processed image into bytes
        _, img_encoded = cv2.imencode('.jpg', img_obj)
        img_bytes = img_encoded.tobytes()
        
        # Img Comparison:
        nparr = np.frombuffer(img_bytes, np.uint8)
        imageA = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        imageB = cv2.imread('static/assets/ref.jpg')
        histA = cv2.calcHist([imageA], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        histB = cv2.calcHist([imageB], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        cv2.normalize(histA, histA)
        cv2.normalize(histB, histB)
        similarity = cv2.compareHist(histA, histB, cv2.HISTCMP_CORREL)
        
        imageA, imageB = resize_to_smallest(imageA, imageB)

        # Convert the images to grayscale
        gray_image1 = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        gray_image2 = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

        # Compute the Structural Similarity Index (SSIM) between the two images
        similarity_index, _ = ssim(gray_image1, gray_image2, full=True)
        
        # Prepare the response
        response = {
            'prediction': prediction_RF[0],
            'image': img_bytes.hex(),
            'sim': similarity,
            'ssim': similarity_index
        }
        
        # Return the prediction result
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@app.route('/greet', methods=['GET'])
def greet():
    return jsonify({'Msg': 'Hello World!'})



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
