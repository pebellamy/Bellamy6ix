#from bellamy import app
from flask import Flask, render_template, url_for, redirect, request, Blueprint, current_app, jsonify
from time import sleep

app = Flask(__name__)
# app.config['DEBUG'] = True # Set this to False for production

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

# Import the route functions from the controlers directory
from controllers.generate_image_controller import generate_image
from controllers.caption_game_controller import caption_game

# Register the blueprints with the Flask app
app.register_blueprint(generate_image)
app.register_blueprint(caption_game)



if __name__ == '__main__':
    # I changed this to run in debug mode so that it will reload when I make changes -> only works if you use python3 app.py instead of flask run for some reason
    app.run()
