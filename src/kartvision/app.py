import sys
from flask import render_template, Flask
from google.cloud import vision
import imagelib

# regions = [(1520, 204, 2125, 1596)]
# client = vision.ImageAnnotatorClient()
imagelib.init()
imagelib.screenshot()

data = [
    {'team':"A", 'points':65},
    {'team':"B", 'points':56},
    {'team':"C", 'points':31},
    {'team':"D", 'points':12},
]

app = Flask(__name__)

@app.route("/")
def results():
    return render_template("result.html", data=data)

@app.route("/history")
def history():
    images = imagelib.get_screenshot()
    return render_template("history.html", images=images)

