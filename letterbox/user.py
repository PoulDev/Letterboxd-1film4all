import requests
from bs4 import BeautifulSoup

from .headers import headers

def parse_films(body):
    parse = BeautifulSoup(body, 'html.parser')
    posters = parse.find('div', class_='poster-grid')

    if posters is None:
        raise ValueError('couldn\'t find posters')
    
    films = {}
    for poster in posters.find_all('li'):
        info = poster.find('div')
        img = poster.find('img')
        if info is None: continue
        if img is None: continue

        films[info['data-item-slug']] = {
            'id': info['data-item-slug'],
            'name': info['data-item-name'],
            'link': info['data-item-link'],
            'details': info['data-details-endpoint'],
            'img': img['src']
        }

    div = parse.find('div', class_='paginate-pages')
    if div is None:
        last_page = 1
    else:
        last_page = div.find_all('li', class_='paginate-page')[-1]
        last_page = int(last_page.text)

    return films, last_page


def _get_films_page(user, page=1):
    body = requests.get(f'https://letterboxd.com/{user}/films/page/{page}', headers=headers)
    
    return parse_films(body.text)

def _get_watchlist_page(user, page=1):
    body = requests.get(f'https://letterboxd.com/{user}/watchlist/page/{page}', headers=headers)
    
    return parse_films(body.text)

def get_films(user):
    films = {}
    current = 1
    total = 2
    while current < total:
        newfilms, total = _get_films_page(user, current)
        current += 1
        films.update(newfilms)

    return films

def get_watchlist(user):
    films = {}
    current = 1
    total = 2
    while current < total:
        newfilms, total = _get_watchlist_page(user, current)
        current += 1
        films.update(newfilms)

    return films

if __name__ == '__main__':
    print('\n'.join(str(x) for x in get_watchlist('Traba128')))
