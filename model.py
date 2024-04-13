from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
load_dotenv()

import os
import google.generativeai as genai


app = Flask(__name__)
CORS(app)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question, chat_history):
    input_prompt = ""   

    input_prompt += "\nChat History:\n"
    for role, text in chat_history:
        input_prompt += f"{role}: {text}\n"

    input_prompt += f"\nQuestion: {question}"

    response = chat.send_message(input_prompt, stream=True)
    return response

@app.route('/answer_question', methods=['POST'])
def chat_endpoint():
    input_prompt = request.json.get('prompt')
    print(input_prompt)
    if not input_prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    # chat_history = request.json.get('chat_history', [])
    chat_history=[]

    response = get_gemini_response(input_prompt,chat_history)
    response_text = ''.join(chunk.text for chunk in response)

    chat_history.append(("You", input_prompt))
    chat_history.append(("Bot", response_text))

    return jsonify({'response': response_text, 'chat_history': chat_history})

if __name__ == '__main__':
    app.run(debug=True)