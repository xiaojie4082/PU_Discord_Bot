import google.generativeai as genai
from load_creds import load_creds

creds = load_creds()
genai.configure(credentials=creds)
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 8192,
  }
safety_settings = []

def freshman_chat(mes:str):
  model = genai.GenerativeModel(model_name="tunedModels/l-7bbcv00s8dia",
                  generation_config=generation_config,
                  safety_settings=safety_settings)
  prompt_parts = [mes]
  response = model.generate_content(prompt_parts)
  return response.text

def gs_chat(mes:str):
  model = genai.GenerativeModel(model_name="gemini-pro",
                  generation_config=generation_config,
                  safety_settings=safety_settings)
  prompt_parts = [mes]
  response = model.generate_content(prompt_parts)
  return response.text

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/freshmanchat', methods=['POST'])
def freshmanchat():
  try:
    data = request.get_json()
    message = data.get('message')
    response = freshman_chat(message)
    return response
  except Exception as e:
    return str(e), 500

@app.route('/gschat', methods=['POST'])
def gschat():
  try:
    data = request.get_json()
    message = data.get('message')
    response = gs_chat(message)
    return response
  except Exception as e:
    return str(e), 500

if __name__ == '__main__':
    app.run()