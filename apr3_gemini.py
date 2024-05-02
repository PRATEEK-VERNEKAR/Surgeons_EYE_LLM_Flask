
from dotenv import load_dotenv
load_dotenv()
import os
from groq import Groq

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client=Groq(
    api_key=os.getenv("LLAMA_KEY")
)


@app.route('/chat', methods=['POST'])
def chat_endpoint():
    input_prompt = request.json.get('prompt')
    if not input_prompt:
        return jsonify({'error': 'Prompt is required'}), 400




    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role":"system",
                "content":"Your name is SurgeonsEYE and you are a surgical assitant bot, you job is to answer the questions related to surgeries"
            },
            # {
            #     "role": "user",
            #     "content": "Incision Phase: (0 seconds - 26 seconds)\n--------------------->Tools Used: Bonn Forceps , Primary Knife , Secondary Knife\n--------------------->Eye parts detected: Cornea, Iris, Cataract Lens , Sclera\nViscous agent injection Phase: (27 seconds - 39 seconds)\n--------------------->Tools Used: Rycroft Cannula , Visco Cannula\n--------------------->Eye parts detected: Cornea, Iris, Cataract Lens ,Sclera \nRhexis Phase: (40 seconds - 74 seconds)\n--------------------->Tools Used: Cap Cystotome , Cap Forceps\n--------------------->Eye parts detected: Cornea, Iris, Lens Fragments, Sclera\nHydrodissection Phase: (75 seconds - 104 seconds)\n--------------------->Tools Used: Hydro Cannula\n--------------------->Eye parts detected: Cornea, Iris, Lens Fragments\nPhacoemulsificiation Phase: (105 seconds - 191 seconds)\n--------------------->Tools Used: Phaco Handpiece\n--------------------->Eye parts detected: Cornea, Lens Fragments, Sclera\nIrrigation and aspiration Phase: (192 seconds - 224 seconds)\n--------------------->Tools Used: A/I Handpiece\n--------------------->Eye parts detected: Cornea, Capsule, Sclera\nCapsule polishing Phase: (225 seconds - 242 seconds)\n--------------------->Tools Used: Rycroft Cannula , Visco Cannula\n--------------------->Eye parts detected: Cornea, Capsule, Sclera\nViscous agent injection Phase: (243 seconds - 251 seconds)\n--------------------->Tools Used: Hydro Cannula , Visco Cannula\n--------------------->Eye parts detected: Cornea, Sclera\nLens implant setting-up Phase: (252 seconds - 276 seconds)\n--------------------->Tools Used: Micromanipulator , Lens Injector\n--------------------->Eye parts detected: Cornea, Artificial Lens, Sclera\nViscous agent removal Phase: (277 seconds - 313 seconds)\n--------------------->Tools Used: Micromanipulator , A/I Handpiece\n--------------------->Eye parts detected: Cornea, Artificial Lens, Sclera\nTonifying and antibiotics Phase: (314 seconds - 332 seconds)\n--------------------->Tools Used: Rycroft Cannula , Visco Cannula\n--------------------->Eye parts detected: Cornea, Artificial Lens, Sclera\n \n\n Tools Motion Information Phase1 Predicted Tools\n--------> Knife moving from Bottom-Center to Bottom-Center\n\nPhase2 Predicted Tools\n--------> Rycroft-Cannula moving from Bottom-Right to Bottom-Center\n\nPhase3 Predicted Tools\n--------> Capsulorhexis-Forceps moving from Bottom-Right to Mid-Right\n\nPhase4 Predicted Tools\n--------> Hydro-Cannula moving from Bottom-Center to Bottom-Center\n\nPhase5 Predicted Tools\n--------> Phacoemulsification-Handpiece moving from Bottom-Center to Mid-Center\n\nPhase6 Predicted Tools\n--------> AI-Handpiece moving from Mid-Right to Mid-Right\n\nPhase7 Predicted Tools\n--------> Rycroft-Cannula moving from Bottom-Left to Bottom-Left\n\nPhase7a Predicted Tools\n--------> Hydro-Cannula moving from Bottom-Right to Bottom-Right\n\nPhase8 Predicted Tools\n--------> Lens-Injector moving from Mid-Right to Bottom-Right\n\n--------> Micromanipulator moving from Bottom-Center to Bottom-Center\n\nPhase9 Predicted Tools\n--------> AI-Handpiece moving from Bottom-Center to Mid-Center\n\nPhase10 Predicted Tools\n--------> Rycroft-Cannula moving from Mid-Right to Bottom-Center\n\n"
            # },
            {
                "role": "user",
                "content": input_prompt
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    text_result=''
    for chunk in completion:
        text_result += chunk.choices[0].delta.content or ""


    print(text_result)
    return jsonify({'response': text_result})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
