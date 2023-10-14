import random
from flask import Blueprint, render_template
from captions import captions

caption_game = Blueprint('caption_game', __name__)

@caption_game.route("/caption-game")
def caption_game_route():
    # Get a random caption
    prompt = random.choice(captions)
    return render_template("caption_game.html", prompt=prompt)
