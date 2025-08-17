# app.py
# This is the backend server that finds and serves memes.

# We need to import the Flask library to create our web server,
# requests to fetch data from the meme API,
# and CORS to allow our HTML frontend to communicate with this server.
from flask import Flask, jsonify
from flask_cors import CORS
import requests
import random

# Initialize the Flask application
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS). This is a security feature
# that allows your HTML file (running on a different "origin") to make
# requests to this Python server.
CORS(app)

# This is the URL of the public API we'll use to get memes.
# It's a simple API that doesn't require an API key.
MEME_API_URL = "https://meme-api.com/gimme"

# Define a "route" for our server. This means when a web browser
# or our frontend asks for the "/get-meme" page, this function will run.
@app.route('/get-meme')
def get_meme():
    """
    Fetches a random meme from the API and returns it as JSON.
    """
    try:
        # Make a GET request to the meme API.
        # The timeout is set to 10 seconds to prevent the server from hanging.
        response = requests.get(MEME_API_URL, timeout=10)
        
        # This will raise an error if the request was not successful (e.g., 404, 500)
        response.raise_for_status()
        
        # Parse the JSON response from the API into a Python dictionary.
        data = response.json()
        
        # We are interested in the meme's title and the image URL.
        # We use .get() as a safe way to access keys that might be missing.
        meme_data = {
            'title': data.get('title', 'No Title'),
            'url': data.get('url', '')
        }
        
        # Check if we actually got a URL.
        if not meme_data['url']:
            return jsonify({"error": "Failed to get a meme URL from the API."}), 500

        # Return the meme data in JSON format with a 200 OK status.
        return jsonify(meme_data)

    except requests.exceptions.RequestException as e:
        # If anything goes wrong with the web request (e.g., network error, timeout),
        # we'll catch the error and return a helpful message.
        print(f"Error fetching meme: {e}")
        return jsonify({"error": "Could not connect to the meme API."}), 503 # Service Unavailable

# This is a standard Python construct. It means:
# "If you run this script directly (not importing it), then run the app."
if __name__ == '__main__':
    # Run the Flask web server.
    # host='0.0.0.0' makes it accessible from other devices on your network.
    # port=5000 is the standard port for Flask development.
    # debug=True will show detailed errors in the browser and auto-reload the server on code changes.
    app.run(host='0.0.0.0', port=5000, debug=True)
