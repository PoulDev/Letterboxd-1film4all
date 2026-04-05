from letterbox.user import get_watchlist, get_films

if __name__ == '__main__':
    names = []
    while True:
        try:
            name = input('Letterboxd Username (CTRL-C to stop) > ')
            names.append(name)
        except KeyboardInterrupt:
            break

    print('\nScraping...')

    users_films = {}
    watchlist = {}
    
    tierlist = [[[] for _ in names] for _ in names]
    # tierlist:
    # how many users watched it
    #     how many users wanna watch it

    for name in names:
        users_films[name] = {}
        print(f'[SCRAPE] Getting {name}\'s watched films...')
        users_films[name]['watched'] = get_films(name)
        print(f'[SCRAPE] Getting {name}\'s watchlist...')
        users_films[name]['watchlist'] = get_watchlist(name)

        watchlist.update(users_films[name]['watchlist'])

    for wannawatch in watchlist:
        N_watchedby = 0
        N_wannawatch = 0
        for user in users_films:
            if wannawatch in users_films[user]['watched']:
                N_watchedby += 1

            if wannawatch in users_films[user]['watchlist']:
                N_wannawatch += 1

        tierlist[N_watchedby][len(names)-N_wannawatch].append(watchlist[wannawatch]['name'])


    for index, tier in enumerate(tierlist):
        print(f'\n\nWATCHED BY {index} USERS')
        if tierlist[index] == []: continue
        for index2, tier2 in enumerate(tierlist[index]):
            if tierlist[index][index2] == []: continue
            print(f'\t{len(names)-index2} USERS WANT TO WATCH THOSE FILMS')
            print('\n'.join('\t\t' + f for f in tierlist[index][index2]))
