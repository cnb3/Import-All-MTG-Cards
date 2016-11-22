import json
from collections import defaultdict
import hashlib
from pymongo import MongoClient

cards =[]

#assume json comes from https://mtgjson.com/json/AllSetsArray-x.json
#documentation from https://mtgjson.com/documentation.html
with open('AllSetsArray-x.json', 'rb') as json_data:
	all_sets = json.load(json_data)
	for current_set in all_sets:
		set_code = current_set.get('code', 'Missing Set Code')

		for current_card in current_set['cards']:
			card = {
				'name': current_card.get('name', "The One Eyed Stranger"),
				'names': current_card.get('names'), #all names on card, for split/flip/etc cards
				'layout': current_card.get('layout'),
				'manaCost': current_card.get('manaCost'),
				'cmc': current_card.get('cmc'),
				'colors': current_card.get('colors'),
				'colorIdentity': current_card.get('colorIdentity'),
				'type': current_card.get('type'),
				'supertypes': current_card.get('supertypes'),
				'types': current_card.get('types'),
				'subtypes': current_card.get('subtypes'),
				'rarity': current_card.get('rarity'),
				'text': current_card.get('text'),
				'flavor': current_card.get('flavor'),
				'artist': current_card.get('artist'),
				'number': current_card.get('number', "XXX"),
				'power': current_card.get('power'),
				'toughness': current_card.get('toughness'),
				'loyalty': current_card.get('loyalty'),
				'multiverseid': current_card.get('multiverseid'), #for linking out to http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=x
				'hand': current_card.get('hand'), #hand and life only on vanguard cards, which we use so, including
				'life': current_card.get('life'),
				'legalities': current_card.get('legalities'),
				'set': set_code
			}

			sha_1 = hashlib.sha1()
    		sha_1.update(card['name'].encode('utf-8') + card['set'].encode('utf-8') + card['number'].encode('utf-8'))
    		card['id'] = sha_1.hexdigest()
    		cards.append(card)

	json_data.close()

client = MongoClient()
db = client['all_cards']

result = db.cards.insert(cards)