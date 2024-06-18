#from flask import Flask, request, jsonify
from flask import Blueprint, request, jsonify
import pandas as pd
from google.cloud import firestore
import os
import jwt
import logging

#app = Flask(__name__)
rec_system_blueprint = Blueprint('rec_system', __name__)
# Set Google Cloud credentials for Firestore
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config/cc-c241-ps246-firebase-adminsdk-jl7du-a56aaeb9d0.json"

# Initialize Firestore client
db = firestore.Client()

# Load the skincare products data
data = pd.read_csv('./cosmetics.csv')

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def verify_token(token):
    """Verify token and return user info."""
    try:
        secret_key = 'bismillahcapstonelancar'  # Update your secret key
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
        email = decoded_token.get('email')
        
        if not email:
            logging.debug("Email not found in token")
            return None

        users_ref = db.collection('users')
        query = users_ref.where('email', '==', email)
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

def filter_products(skin_type):
    if skin_type.lower() == "oily":
        return data[data["Oily"] == 1]
    elif skin_type.lower() == "dry":
        return data[data["Dry"] == 1]
    elif skin_type.lower() == "sensitive":
        return data[data["Sensitive"] == 1]
    elif skin_type.lower() == "combination":
        return data[data["Combination"] == 1]
    elif skin_type.lower() == "normal":
        return data[data["Normal"] == 1]
    else:
        return pd.DataFrame()

#@app.route('/recommendSkintype', methods=['GET'])
@rec_system_blueprint.route('/recommend', methods=['GET'])
def recommend():
    auth_header = request.headers.get('Authorization', '')

    if not auth_header or 'Bearer ' not in auth_header:
        return jsonify({'error': 'Authorization header is missing or not valid'}), 401

    token = auth_header.split(' ')[1]
    user_data = verify_token(token)
    if not user_data:
        return jsonify({'error': 'Invalid or expired token'}), 401

    skin_type = user_data.get('skin_type', '')
    print(skin_type)
    if not skin_type:
        return jsonify({'error': 'Skin type not found for the given user'}), 404

    filtered_data = filter_products(skin_type)
    if filtered_data.empty:
        return jsonify({'error': 'No products found for the given skin type'}), 404

    recommendations = filtered_data.to_dict(orient='records')
    return jsonify(recommendations)

#if __name__ == '__main__':
#    app.run(debug=True)
