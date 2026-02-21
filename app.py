from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import numpy as np
from PIL import Image
from dotenv import load_dotenv
from groq import Groq



load_dotenv()

app = Flask(__name__)

CORS(app)



UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)



client = Groq(api_key="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")



@app.route("/")

def index():

    return render_template("index.html")



@app.route("/analyze", methods=["POST"])

def analyze():

    file = request.files["image"]

    gender = request.form.get("gender")



    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    file.save(filepath)



    img = Image.open(filepath).convert("RGB")

    arr = np.array(img)

    avg_color = arr.mean(axis=(0,1))

    skin_rgb = tuple(map(int, avg_color))



    prompt = f"""

    Suggest fashion styling tips for a {gender} with skin tone RGB {skin_rgb}.

    Give dress colors, outfit, shoes, accessories.

    """



    chat = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[{"role": "user", "content": prompt}],

        temperature=0.7,

        max_tokens=1200

    )



    recommendation = chat.choices[0].message.content



    return jsonify({

        "skin_rgb": skin_rgb,

        "recommendation": recommendation

    })



if __name__ == "__main__":

    app.run(debug=True)  