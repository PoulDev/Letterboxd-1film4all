import requests

from .headers import headers

def get_details(film):
    res = requests.get(f'https://letterboxd.com/film/{film}/json', headers=headers)
    return res.json()

def get_poster(film):
    res = requests.get(f'https://letterboxd.com/film/{film}/poster/std/70/', headers=headers)
    return res.json()
