from dotenv import load_dotenv
import openai
from time import sleep
import os
from flask import Blueprint, jsonify, current_app, request

generate_image = Blueprint('generate_image', __name__)

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

@generate_image.route("/generate-image", methods=["POST"])
def generate_image_route():
    user_prompt = request.form.get('prompt')
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
