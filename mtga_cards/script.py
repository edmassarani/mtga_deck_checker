import json
import requests

CURRENT_STANDARD_SETS = ['RNA', 'GRN', 'M19', 'DOM', 'RIX', 'XLN', 'ANA']

BASE_URL = 'https://api.scryfall.com'


def get_set_data(code):
    url = BASE_URL + '/cards/search?order=set&q=e%3A' + code + '&unique=prints'
    data = []
    page = 1
    res = requests.get(url=url).json()
    data += res['data']

    while res['has_more']:
        page += 1
        res = requests.get(url=res['next_page']).json()
        data += res['data']

    return data


data = []
for setName in CURRENT_STANDARD_SETS:
    data += get_set_data(setName)

cards = {}

names = {}

for card in data:
    if 'arena_id' in card:
        if card['layout'] == 'transform':
            names[card['card_faces'][0]['name']] = card['arena_id']
        else:
            names[card['name']] = card['arena_id']
        cards[card['arena_id']] = card

with open('cards.json', 'w') as outfile:
    json.dump({'cards': cards, 'names': names}, outfile)
