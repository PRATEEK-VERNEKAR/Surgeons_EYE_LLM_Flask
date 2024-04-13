# from dotenv import load_dotenv
# load_dotenv()

# import os
# import google.generativeai as genai

# from flask import Flask, request, jsonify

# app = Flask(__name__)

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# model = genai.GenerativeModel("gemini-pro")
# chat = model.start_chat(history=[])

# def get_gemini_response(question, chat_history):
#     print(question)

#     response = chat.send_message(question, stream=True)
#     return response

# @app.route('/chat', methods=['POST'])
# def chat_endpoint():
#     input_prompt = request.json.get('prompt')
#     if not input_prompt:
#         return jsonify({'error': 'Prompt is required'}), 400

#     chat_history = request.json.get('chat_history', [])

#     response = get_gemini_response(input_prompt, chat_history)
#     response_text = ''.join(chunk.text for chunk in response)

#     chat_history.append(("You", input_prompt))
#     chat_history.append(("Bot", response_text))

#     return jsonify({'response': response_text, 'chat_history': chat_history})

# if __name__ == '__main__':
#     app.run(debug=True,port=5000)




from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import flask_cors

app = Flask(__name__)
CORS(app)  # Allow all origins, or replace with: CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# def get_gemini_response(question, chat_history):
#     print(question)
#     response = chat.send_message(question, stream=True)
#     return response

def get_gemini_response(question, chat_history):
    input_str="You are a surgical video analyst. Please analyze the following with the phase duration information, tool information given : "+question+"\n\nProvide your analysis in 4-5 lines, focusing only on medical aspects and avoiding non-medical topics."
    response = chat.send_message(input_str)
    print(response)
    response_text = response
    return response_text

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    input_prompt = request.json.get('prompt')
    if not input_prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    chat_history = request.json.get('chat_history', [])
    response = get_gemini_response(input_prompt, chat_history)
    response_text = ''.join(chunk.text for chunk in response)
    chat_history.append(("You", input_prompt))
    chat_history.append(("Bot", response_text))

    return jsonify({'response': response_text, 'chat_history': chat_history})

if __name__ == '__main__':
    app.run(debug=True, port=5000)