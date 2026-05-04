import sqlite3
import requests




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
    season INTEGER,
    episode INTEGER,
    finished INTEGER
    )
    """)
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
    episodes = response.json()
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
    episodes = response.json()
    if season== 0 and episode== 0:
        return (tvmaze_id,season,episode)
    for i, ep in enumerate(episodes): 
        if ep["season"] == season and ep["number"] == episode:
            if i-1 < 0 :
                return (tvmaze_id,season,episode)  
            next_episode = episodes[i-1]
            return (tvmaze_id,next_episode["season"],next_episode["number"])
    return (tvmaze_id,season,episode)

def max_season(tvmaze_id):
    response = requests.get(f"https://api.tvmaze.com/shows/{tvmaze_id}/episodes")
    episodes = response.json()
    max_season = 0
    for ep in episodes:
        if ep["season"] > max_season:
            max_season = ep["season"]
    return max_season

def max_episode(tvmaze_id,last_season):
    response = requests.get(f"https://api.tvmaze.com/shows/{tvmaze_id}/episodes")
    episodes = response.json()
    max_episode = 0
    for ep in episodes:
        if ep["number"] > max_episode and ep["season"] == last_season:
            max_episode = ep["number"]
    return max_episode

def new_episodes(tvmaze_id, season, episode):
    new = []
    response = requests.get(f"https://api.tvmaze.com/shows/{tvmaze_id}/episodes")
    episodes = response.json()
    for ep in episodes:
        if ep["season"] > season:
            new.append(ep)
        elif ep["season"] == season and ep["number"] > episode:
            new.append(ep)
    return new