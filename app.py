from flask import Flask, render_template, request, redirect, url_for
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
    conn, cur = helpers.get_db()
    ##################
    show_id = request.args.get("id")
    response = requests.get(f"https://api.tvmaze.com/shows/{show_id}")
    data = response.json()
    #######################
    rows = cur.execute("SELECT * FROM library WHERE tvmaze_id = ?", (show_id,)).fetchall()
    conn.close()
    ######################
    saved = bool(rows)
    #######################
    return render_template("details.html",show = data,saved = saved)

@app.route("/library", methods=["GET"])
def library():
    #############DB CURSOR#############
    conn, cur = helpers.get_db()
    rows = cur.execute("SELECT * FROM library").fetchall()
    conn.close()
    #############
    return render_template("library.html",rows = rows)

@app.route("/updates", methods=["GET"])
def updates():
    return render_template("updates.html")

@app.route("/save", methods=["POST"])
def save():
    conn, cur = helpers.get_db()
    #########
    tvmaze = request.form.get("id")
    name = request.form.get("name")
    image = request.form.get("image")
    status = request.form.get("status")
    premiered = request.form.get("premiered")
    cur.execute("INSERT INTO library (tvmaze_id,name,image_url,status,premiered) VALUES (?,?,?,?,?)",(tvmaze,name,image,status,premiered))
    conn.commit()
    conn.close()
    ###########
    response = requests.get(f"https://api.tvmaze.com/shows/{tvmaze}")
    data = response.json()
    ###########
    return redirect(url_for("details",id=tvmaze,saved=True))
    

if __name__ == "__main__":
    app.run(debug=True)