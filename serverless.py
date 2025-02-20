from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Serverless chatbot API details
CHATBOT_API_URL = "https://<serverless-api-base-url>/chat"  # Replace with full API URL if known
API_KEY = "SIUI2F73CNZLWDKPZPLTY2LB7GWM45TSO6DA"

@app.route('/chat', methods=['POST'])
def chat_with_bot():
    user_message = request.json.get("message")

    # Ensure there's a user message before proceeding
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "message": user_message
    }

    # Send request to the serverless chatbot API
    try:
        response = requests.post(CHATBOT_API_URL, headers=headers, json=data)
        response.raise_for_status()
        chatbot_response = response.json()
        return jsonify({"response": chatbot_response})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
