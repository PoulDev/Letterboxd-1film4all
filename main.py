import time
import hashlib

from flask import Flask, render_template, request

from letterbox.film import get_details, get_poster
from letterbox.user import get_films, get_watchlist

app = Flask(__name__)

cached_funcs = {}

def cache(for_=60 * 10):
    def decorator(func):
        def wrapper(*args, **kwargs):
            id_ = hashlib.sha256(f'{func.__name__}{args}{kwargs}'.encode()).hexdigest()
            if id_ in cached_funcs and (time.time() - cached_funcs[id_]["last_update"]) < for_:
                return cached_funcs[id_]["out"]
            
            out = func(*args, **kwargs)
            cached_funcs[id_] = {
                "out": out,
                "last_update": time.time(),
            }
            return out
        return wrapper
    return decorator

get_films = cache()(get_films)
get_watchlist = cache()(get_watchlist)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/letterbox")
def letterbox():
    return render_template("letterbox.html")


@app.route("/letterbox", methods=["POST"])
def letterbox_api():
    data = request.get_json()
    names = data["names"]
    users_films = {}
    watchlist = {}

    tierlist = [[[] for _ in names] for _ in names]

    for name in names:
        users_films[name] = {}

        print(f"[SCRAPE] Getting {name}'s watched films...")
        users_films[name]["watched"] = get_films(name)
        print(f"[SCRAPE] Getting {name}'s watchlist...")
        users_films[name]["watchlist"] = get_watchlist(name)

        watchlist.update(users_films[name]["watchlist"])

    for wannawatch in watchlist:
        N_watchedby = 0
        N_wannawatch = 0
        for user in users_films:
            if wannawatch in users_films[user]["watched"]:
                N_watchedby += 1

            if wannawatch in users_films[user]["watchlist"]:
                N_wannawatch += 1

        tierlist[N_watchedby][len(names) - N_wannawatch].append(watchlist[wannawatch])

    return tierlist


@app.route("/film/<name>/json/")
@app.route("/film/<name>/json")
def film_proxy(name):
    return get_details(name)

@app.route("/film/<name>/poster")
@cache(60 * 60 * 24 * 30)
def film_poster(name):
    print('---- GETTING POSTER FOR', name, '----')
    return get_poster(name)

if __name__ == "__main__":
    app.run(debug=True)
