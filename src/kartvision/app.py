import sys
from flask import render_template, Flask

data = [
    {'team':"A", 'points':65},
    {'team':"B", 'points':56},
    {'team':"C", 'points':31},
    {'team':"D", 'points':12},
]

app = Flask(__name__)

@app.route("/")
def results():
    return render_template("results.html",data=data)
