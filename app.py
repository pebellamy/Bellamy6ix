#from bellamy import app
from flask import Flask, render_template, url_for, redirect, request, Blueprint

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run()
