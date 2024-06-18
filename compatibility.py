#from flask import Flask, request, jsonify
from flask import Blueprint, request, jsonify
import pandas as pd
from google.cloud import firestore
from ingredientOCR import extract_ingredients  # Import the function to extract ingredients
import os  # Ensure os is imported
import jwt  # Import PyJWT library
import logging  # Import logging

#app = Flask(__name__)
compatibility_blueprint = Blueprint('compatibility', __name__)
# Set Google Cloud credentials for Firestore
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config/cc-c241-ps246-firebase-adminsdk-jl7du-a56aaeb9d0.json"

# Load the ingredient data
data = pd.read_csv('ingredient_analysis.csv')

# Initialize Firestore client
db = firestore.Client()

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def check_compatibility(ingredients_list, skin_type, data, avoided_ingredients):
    if isinstance(ingredients_list, str):  # Check if there was an error in ingredient extraction
        return ingredients_list

    for ingredient in ingredients_list:
        for avoided in avoided_ingredients:
            if avoided.lower() in ingredient.lower():
                return f"Not compatible because {ingredient} is an avoided ingredient."

    for ingredient in ingredients_list:
        if ingredient in data['Ingredient'].values:
            if data.loc[data['Ingredient'] == ingredient, skin_type].values[0] == 0:
                return f"Not compatible because {ingredient} is not recommended for {skin_type} skin."

    return "Compatible!"

def verify_token(token):
    """Verify token and return user info."""
    try:
        secret_key = 'bismillahcapstonelancar'  # Your secret key
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
        email = decoded_token.get('email')
        
        if not email:
            logging.debug("Email not found in token")
            return None

        users_ref = db.collection('users')
        query = users_ref.where('token.auth', '==', token)
        results = query.stream()
        user_data = None

        for doc in results:
            user_data = doc.to_dict()
            break

        return user_data
    except jwt.ExpiredSignatureError:
        logging.debug("Token expired")
        return None
    except jwt.InvalidTokenError:
        logging.debug("Invalid token")
        return None

#@app.route('/check_compatibility', methods=['POST'])
@compatibility_blueprint.route('/check_compatibility', methods=['POST'])
def check_compatibility_api():
    gcs_uri = request.json.get('image_uri', 'gs://cc-c241-ps246.appspot.com/images-OCR/images.jpg')
    auth_header = request.headers.get('Authorization', '')

    if not auth_header or 'Bearer ' not in auth_header:
        return jsonify({'result': 'Authorization header is missing or not valid'}), 401

    token = auth_header.split(' ')[1]

    # Verify token and fetch user data
    user_data = verify_token(token)
    if not user_data:
        return jsonify({'result': 'Invalid or expired token'}), 401

    # Extract ingredients from the image
    ingredients_to_check, success = extract_ingredients(gcs_uri)
    if not success:
        return jsonify({'result': ingredients_to_check})

    skin_type = user_data.get('skin_type', '')
    print(skin_type)
    avoided_ingredients = user_data.get('avoided_ingredients', [])
    print(avoided_ingredients)
    result = check_compatibility(ingredients_to_check, skin_type, data, avoided_ingredients)

    return jsonify({'result': result})

#if __name__ == '__main__':
   # app.run(debug=True)
