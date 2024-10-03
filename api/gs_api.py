import google.generativeai as genai
from load_creds import load_creds

creds = load_creds()
genai.configure(credentials=creds)
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "max_output_tokens": 200
}
safety_settings = []

def pu_chat(mes:str):
  model = genai.GenerativeModel(model_name="tunedModels/v2-sxgx8cmt1bgn",
  # model = genai.GenerativeModel(model_name="tunedModels/f-afisjjghb1pa",
                  generation_config=generation_config,
                  safety_settings=safety_settings)
  prompt_parts = [mes]
  response = model.generate_content(prompt_parts)
  return response.text

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/puchat', methods=['POST'])
def freshmanchat():
  try:
    data = request.get_json()
    message = data.get('message')
    response = pu_chat(message)
    return response
  except Exception as e:
    return str(e), 500

if __name__ == '__main__':
    app.run()