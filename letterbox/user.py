import requests
from bs4 import BeautifulSoup

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
    body = requests.get(f'https://letterboxd.com/{user}/films/page/{page}', headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "DNT": "1",
        "Priority": "u=0, i",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "TE": "trailers"
    })
    
    return parse_films(body.text)

def _get_watchlist_page(user, page=1):
    body = requests.get(f'https://letterboxd.com/{user}/watchlist/page/{page}', headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "DNT": "1",
        "Priority": "u=0, i",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "TE": "trailers"
    })
    
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
