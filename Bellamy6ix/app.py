from bellamy import app
from flask import Flask, render_template, url_for, redirect, request, Blueprint

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run()
