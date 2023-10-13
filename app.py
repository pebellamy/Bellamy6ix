#from bellamy import app
from flask import Flask, render_template, url_for, redirect, request, Blueprint, current_app, jsonify
from time import sleep
from dotenv import load_dotenv
import os
import openai
from captions import captions
import random

load_dotenv()

app = Flask(__name__)
# app.config['DEBUG'] = True # Set this to False for production

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/recies")
def recipes():
    return render_template("recipes.html")


@app.route("/photos")
def photos():
    return render_template("photos.html")

@app.route("/ffa")
def ffa():
    return render_template("ffa.html")

@app.route("/caption-game")
def caption_game():
    # Get a random caption
    prompt = random.choice(captions)
    return render_template("caption_game.html", prompt=prompt)

@app.route("/generate-image", methods=["POST"])
def generate_image():
    user_prompt = request.form.get('prompt')
    caption = "Wednesday's, am i right?"
    full_prompt = f"""
     Illustrate in the style of a New Yorker cartoon: '{user_prompt}'. Please ensure there's no caption or text in the image.
    """
    if current_app.config['DEBUG']:
        # Mock a delay
        sleep(3)
        # Mock API response from Open AI API (https://platform.openai.com/docs/guides/images/usage)
        mock_response = {
            'data': [
                {
                    'url': "https://lilKyleStore.b-cdn.net/debug/DALL%C2%B7E%202023-10-11%2012.45.11%20-%20Comic-style%20drawing%20of%20a%20moonlit%20old%20monastery%20courtyard%20with%20cobblestone%20paths.%20Stone%20statues%20of%20angels%20with%20eerie%20expressions%20stand%20among%20ivy-covere.png"
                }
            ]
        }
        image_url = mock_response['data'][0]['url']
    else:
        # Use OpenAI's API to get the image based on the prompt

        response = openai.Image.create(
            prompt=full_prompt,
            n=1,
            size="1024x1024",
        )
        image_url = response['data'][0]['url']
        pass
    return jsonify({'image_url': image_url})

if __name__ == '__main__':
    # I changed this to run in debug mode so that it will reload when I make changes -> only works if you use python3 app.py instead of flask run for some reason
    app.run()
