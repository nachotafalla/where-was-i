from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    response = requests.get("https://api.tvmaze.com/search/shows?", params={"q": query})
    data = response.json()
    return render_template("search.html",results=data)
    
@app.route("/details", methods=["GET"])
def details():


if __name__ == "__main__":
    app.run(debug=True)