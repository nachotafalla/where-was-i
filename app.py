from flask import Flask, render_template, request
import requests
import sqlite3
import helpers

app = Flask(__name__)
#### DATABASE
helpers.startdb()
###################


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["GET"])
def search():
    if not request.args.get("query"):
        return render_template("search.html",results = [])
    query = request.args.get("query")
    response = requests.get("https://api.tvmaze.com/search/shows?", params={"q": query})
    data = response.json()
    print(data)
    return render_template("search.html",results=data)
    
@app.route("/details", methods=["GET"])
def details():
    show_id = request.args.get("id")
    response = requests.get(f"https://api.tvmaze.com/shows/{show_id}")
    data = response.json()
    return render_template("details.html",show = data)

@app.route("/library", methods=["GET"])
def library():
    #############DB CURSOR#############
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    rows = cur.execute("""SELECT * FROM library""").fetchall()
    conn.close()
    #############
    return render_template("library.html",rows = rows)

@app.route("/updates", methods=["GET"])
def updates():
    return render_template("updates.html")

if __name__ == "__main__":
    app.run(debug=True)