import sqlite3
import requests
from datetime import date




def startdb():
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS library (id INTEGER PRIMARY KEY AUTOINCREMENT,
    tvmaze_id INTEGER NOT NULL UNIQUE,
    name TEXT NOT NULL,
    image_url TEXT,
    status TEXT,
    premiered TEXT,
    season INTEGER DEFAULT 0,
    episode INTEGER DEFAULT 0,
    finished INTEGER DEFAULT 0
    )
    """)
    cur.execute("UPDATE library SET season = 0 WHERE season IS NULL")
    cur.execute("UPDATE library SET episode = 0 WHERE episode IS NULL")
    cur.execute("UPDATE library SET finished = 0 WHERE finished IS NULL")
    conn.commit()
    conn.close()

def imagefb(image):
    if image:
        return image["medium"]
    else:
        return ""

def get_db():
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    return conn, cur

def close_db(conn):
    conn.commit()
    conn.close()

def next_ep(tvmaze_id,season,episode):
    response = requests.get(f"https://api.tvmaze.com/shows/{tvmaze_id}/episodes")
    if response.status_code != 200:
        return (tvmaze_id, season, episode)
    episodes = response.json()
    if not episodes:
        return (tvmaze_id, season, episode)
    if season== 0 and episode== 0:
        return (tvmaze_id,episodes[0]["season"],episodes[0]["number"])
    for i, ep in enumerate(episodes): 
        if ep["season"] == season and ep["number"] == episode:
            if i+1 >= len(episodes):
                return (tvmaze_id,season,episode)  
            next_episode = episodes[i+1]
            return (tvmaze_id,next_episode["season"],next_episode["number"])
    return (tvmaze_id,season,episode)

def prev_ep(tvmaze_id,season,episode):
    response = requests.get(f"https://api.tvmaze.com/shows/{tvmaze_id}/episodes")
    if response.status_code != 200:
        return (tvmaze_id,season,episode)
    episodes = response.json()
    if not episodes:
        return (tvmaze_id, season, episode)
    if season== 0 and episode== 0:
        return (tvmaze_id,season,episode)
    for i, ep in enumerate(episodes): 
        if ep["season"] == season and ep["number"] == episode:
            if i-1 < 0 :
                return (tvmaze_id,0,0)  
            previous_episode = episodes[i-1]
            return (tvmaze_id,previous_episode["season"],previous_episode["number"])
    return (tvmaze_id,season,episode)

def max_season(tvmaze_id):
    response = requests.get(f"https://api.tvmaze.com/shows/{tvmaze_id}/episodes")
    if response.status_code != 200:
        return 0
    episodes = response.json()
    max_season = 0
    for ep in episodes:
        if ep["season"] > max_season:
            max_season = ep["season"]
    return max_season

def max_episode(tvmaze_id,last_season):
    response = requests.get(f"https://api.tvmaze.com/shows/{tvmaze_id}/episodes")
    if response.status_code != 200:
        return 0
    episodes = response.json()
    max_episode = 0
    for ep in episodes:
        if ep["number"] > max_episode and ep["season"] == last_season:
            max_episode = ep["number"]
    return max_episode

def new_episodes(tvmaze_id, season, episode):
    new = []
    response = requests.get(f"https://api.tvmaze.com/shows/{tvmaze_id}/episodes")
    if response.status_code != 200:
        return []
    episodes = response.json()
    for ep in episodes:
        if not ep["airdate"]:
            continue
        airdate = date.fromisoformat(ep["airdate"])
        if airdate > date.today():
            continue
        if ep["season"] > season:
            new.append(ep)
        elif ep["season"] == season and ep["number"] > episode:
            new.append(ep)
    return new

def search_rank(result, query):
    name = result["show"]["name"].lower()
    q = query.lower()

    rating = result["show"]["rating"]["average"]
    if not rating:
        rating = 0

    rank = 0

    if name == q:
        rank += 100

    if name.startswith(q):
        rank += 25

    if q in name:
        rank += 40

    rank += rating * 10
    rank += result["score"]

    return rank