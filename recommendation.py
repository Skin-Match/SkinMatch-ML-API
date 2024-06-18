from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load the dataset
data = pd.read_csv('cosmetics.csv')

# Prepare the TF-IDF vectorizer and compute cosine similarity matrix
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(data['Name'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to get recommendations based on product name
def get_recommendations(product_name, cosine_sim=cosine_sim):
    # Get the index of the product that matches the name
    try:
        idx = data[data['Name'].str.contains(product_name, case=False)].index[0]
    except IndexError:
        return []

    # Get the pairwise similarity scores of all products with that product
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the products based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar products
    sim_scores = sim_scores[1:11]

    # Get the product indices
    product_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar product names
    return data.iloc[product_indices]['Name'].tolist()

# Define the API endpoint
@app.route('/recommendationz', methods=['POST'])
def recommend():
    product_name = request.json.get('product_name')
    recommendations = get_recommendations(product_name)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
