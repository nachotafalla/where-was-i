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
    show_id = request.args.get("id")
    response = requests.get(f"https://api.tvmaze.com/shows/{show_id}")
    data = response.json()
    return render_template("details.html",results = data)

@app.route("/library", methods=["GET"])
def library():
    return render_template("library.html")

@app.route("/updates", methods=["GET"])
def library():
    return render_template("library.html")

if __name__ == "__main__":
    app.run(debug=True)