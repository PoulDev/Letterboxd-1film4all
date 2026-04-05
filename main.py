import time

from flask import Flask, render_template, request

from letterbox.film import get_details, get_poster
from letterbox.user import get_films, get_watchlist

app = Flask(__name__)

cache = {}


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

        if name in cache and (time.time() - cache[name]["last_update"]) < 60 * 10:
            users_films[name]["watched"] = cache[name]["watched"]
            users_films[name]["watchlist"] = cache[name]["watchlist"]
        else:
            print(f"[SCRAPE] Getting {name}'s watched films...")
            users_films[name]["watched"] = get_films(name)
            print(f"[SCRAPE] Getting {name}'s watchlist...")
            users_films[name]["watchlist"] = get_watchlist(name)

            cache[name] = {
                "watched": users_films[name]["watched"],
                "watchlist": users_films[name]["watchlist"],
                "last_update": time.time(),
            }

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
def film_poster(name):
    return get_poster(name)

if __name__ == "__main__":
    app.run(debug=True)
