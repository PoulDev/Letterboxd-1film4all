# Letterboxd-1film4all
Find a film everyone agrees on by combining multiple users watchlist and watched films.

## How this works
The program takes a list of letterboxd usernames as input, it loads their watchlists and watched films,
and it makes a tierlist of possible films to watch.

The tierlist structure is the following:
watched by x users:
    y users want to watch those films:
        ...film1...
        ...film2...

So there are two orderings for the films: first by the number of users that watched the films, and the second one is by the number of users that want to watch the listed films.

## How to run:
There are two versions of the program, one for the terminal and one for the web.

**Setup:**
```bash
# Clone the repository
git clone https://github.com/PoulDev/Letterboxd-1film4all.git
cd Letterboxd-1film4all

# Create the virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the dependencies
pip install -r requirements.txt
```

**Run the terminal version:**
```bash
python cli.py
```

**Run the web version:**
```bash
python main.py
```

Then open your browser and go to `http://localhost:5000/`

> \[!NOTE]
> The web version is built for local usage only, I wouldn't recommend hosting it for the public.
> But if you whish to do that anyway you should implement some proxies, if you don't want to get your server's IP banned for dossing.

---

This program has been made by an human, no AI has been used ;3.
