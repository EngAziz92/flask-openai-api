from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os



# Initialize Flask app
app = Flask(__name__)

# Enable CORS
CORS(app)

# Set OpenAI API Key from environment variable
import os
openai.api_key = os.getenv("OPENAI_API_KEY")



@app.route('/get_past_participle', methods=['GET', 'POST'])
def get_past_participle():
    if request.method == 'POST':
        data = request.json
        german_verb = data.get('verb')
    elif request.method == 'GET':
        german_verb = request.args.get('verb')

    # Validate input
    if not german_verb or not isinstance(german_verb, str) or german_verb.strip() == "":
        return jsonify({"error": "A valid 'verb' is required"}), 400

    try:
        # Make OpenAI API request
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in German grammar."},
                {"role": "user", "content": f"What is the past participle of the German verb '{german_verb}'?"}
            ]
        )
        # Extract the assistant's reply
        past_participle = response['choices'][0]['message']['content'].strip()

        return jsonify({"verb": german_verb, "past_participle": past_participle})
    except openai.error.OpenAIError as e:
        # Handle OpenAI-specific errors
        return jsonify({"error": f"OpenAI API Error: {str(e)}"}), 500
    except Exception as e:
        # Handle general exceptions
        return jsonify({"error": f"Server Error: {str(e)}"}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
