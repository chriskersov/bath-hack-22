from flask import Flask, render_template, request,  session, redirect, g, flash, url_for, send_from_directory, jsonify

from flask_session import Session
import sqlite3
import os

from datetime import datetime
from datetime import date

######################## For Files, trial #################
from werkzeug.utils import secure_filename
from PIL import Image # Used to save processed images.
import sqlite3 # Used to initialise the db.
import os
import requests  # REST API interaction
import time
from urllib.parse import quote  # For URL encoding
from datetime import datetime
app = Flask(__name__)

START_PAGE = "start.html"
MAIN_PAGE = "show.html"
END_PAGE = "win.html"

IMAGES = [
    "/images/Wordle.png",
    "/images/Wordle.png",
    "/images/Wordle.png"
]

OPTIONS = [
    "Fabio",
    "Guy A",
    "IDK"
]

@app.route("/PLACEHOLDER/Prepare/", methods = ["GET"])
def start():
    return render_template(START_PAGE, options=list(zip(OPTIONS, IMAGES)), questions=5)

@app.route("/PLACEHOLDER/Gameshow/", methods = ["GET, POST"])
def showtime():
    render_template(MAIN_PAGE)

@app.route("/PLACEHOLDER/Finale/", methods = ["GET"])
def victory():
    render_template(END_PAGE)






if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)