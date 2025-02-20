import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# URL for the Vultr Inference API endpoint
api_url = 'https://api.vultrinference.com/v1/chat/completions'

# Your API key (replace with your actual key)
api_key = 'SIUI2F73CNZLWDKPZPLTY2LB7GWM45TSO6DA'

# Headers for the request (including the authorization token)
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}

# Route for the chatbot interaction
@app.route('/chat', methods=['POST'])
def chatbot():
    # Get the message from the request body
    user_input = request.json.get('message')
    
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400
    
    # Request body for the Vultr inference API
    payload = {
        'model': 'alpaca-native-Q5_K_M',  # Replace with your selected model
        'messages': [
            {'role': 'user', 'content': user_input}  # Only send the user message
        ],
        'temperature': 0.7,
        'max_tokens': 150
    }

    # Send POST request to Vultr Inference API
    response = requests.post(api_url, json=payload, headers=headers)

    # Check for success
    if response.status_code == 200:
        response_json = response.json()
        
        # Optionally save the response to a file for later inspection
        with open('full_response.json', 'w') as f:
            json.dump(response_json, f, indent=4)
        
        # Extract and send back the chatbot's message response
        if "choices" in response_json:
            chatbot_message = response_json["choices"][0]["message"]["content"]
            return jsonify({"response": chatbot_message})
        else:
            return jsonify({"error": "No response from model"}), 500
    else:
        # Log the error response from Vultr for debugging
        response_json = response.json()
        return jsonify({'error': f'Failed to get response from Vultr. Status code: {response.status_code}', 'details': response_json}), response.status_code

# Simple route to check if the server is running
@app.route('/')
def home():
    return "Flask server is running!"

# Start the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
