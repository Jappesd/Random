# tkintar app for display
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return "Dashboard Home"


if __name__ == "__main__":
    app.run(debug=True)
