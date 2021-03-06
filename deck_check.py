import win32clipboard
import json
import sys
import os
import re


class DeckChecker:
    # keyword for getting collection from log
    KEYWORD = "PlayerInventory.GetPlayerCardsV3"

    # log's location on the computer
    LOG_LOCATION = os.getenv(
        'APPDATA') + "\\..\\LocalLow\\Wizards Of The Coast\\MTGA\\output_log.txt"

    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
        cards_path = os.path.abspath(os.path.join(
            application_path, '..', 'cards.json'))
    elif __file__:
        application_path = os.path.dirname(__file__)
        cards_path = os.path.abspath(
            os.path.join(application_path, 'cards.json'))

    STANDARD_CARDS = json.load(open(cards_path))

    def get_collection(self):
        # open logfile in reading mode
        logfile = open(self.LOG_LOCATION, "r")

        # variable for starting to record file's data
        start = False

        # variable for storing the data
        # card name => [quantity, card data]
        collection = {}

        # loop through each line and save only the ones that are
        # between the keyword and the closing bracket
        for line in logfile:
            if line.find("<== " + self.KEYWORD) > -1:
                start = True
            if start and line.find(':') > -1:
                line = line.strip()
                # line = "12345: 1" (5 number id and quantity)
                cardId = line[1:6]
                card = self.STANDARD_CARDS['cards'][cardId]
                quantity = int(line[9])
                collection[card['name']] = [quantity, card]
            if line.find('}') > -1:
                start = False

        logfile.close()

        return collection

    def get_wild_cards(self):
        logfile = open(self.LOG_LOCATION, "r")
        match = '<== PlayerInventory.GetPlayerInventory'
        start = False

        string = ''

        for line in logfile:
            if start and line.find('[U') > -1:
                break
            if start:
                string += line
            if line.find(match) > -1:
                start = True

        data = json.loads(string)

        return {
            'common': data['wcCommon'],
            'uncommon': data['wcUncommon'],
            'rare': data['wcRare'],
            'mythic': data['wcMythic']
        }

    def get_deck(self):
        # get the desired deck from the clipboard
        win32clipboard.OpenClipboard()
        clipboard = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()

        # split the data into a list
        dirtyDeck = clipboard.strip().split('\r\n')

        dirtySideBoard = []
        # separate sideboard
        if '' in dirtyDeck:
            idx = dirtyDeck.index('')
            dirtySideBoard = dirtyDeck[idx + 1:]
            dirtyDeck = dirtyDeck[:idx]

        return [dirtyDeck, dirtySideBoard]

    def filter_deck(self, dirtyDeck):
        # variable for storing desired deck and sideboard
        # card name => quantity
        mainDeck = self.filter_cards(dirtyDeck[0])
        sideBoard = []

        if dirtyDeck[1]:
            sideBoard = self.filter_cards(dirtyDeck[1])

        return [mainDeck, sideBoard]

    def filter_cards(self, dirtyDeck):
        deck = {}
        # loop through each card and save them if they are valid
        for card in dirtyDeck:
            if not re.match(r'\d{1,2} .* \([A-Z0-9]{3}\) .*', card):
                print('Invalid deck')
                print('(' + card + ')\nIs not a card')
                input('Press <Enter> to try again')
                self.__init__()
            card = card.split(' ')
            quantity = int(card[0])
            for idx, val in enumerate(card):
                if re.match(r'\([A-Z0-9]{3}\)', val):
                    stopName = idx
                    break
            name = ' '.join(card[1:stopName])
            deck[name] = quantity

        return deck

    def print_data(self, deck, collection):
        wildcards = self.get_wild_cards()
        self.print_info(deck[0], collection, wildcards, 'main deck')
        if deck[1]:
            self.print_info(deck[1], collection, wildcards, 'sideboard')

    def print_info(self, deck, collection, wildcards, text):
        missing = {
            "common": 0,
            "uncommon": 0,
            "rare": 0,
            "mythic": 0,
        }

        # loop through each card in the main deck
        for name, desired in deck.items():
            # check if they exist in the colection or if it's a basic land
            # get the owned quantity of the card
            if name in collection:
                data = collection[name]
                owned = data[0]
                card = data[1]
                rarity = card['rarity']
            elif name in ['Mountain', 'Forest', 'Plains', 'Island', 'Swamp']:
                owned = desired
            else:
                owned = 0
                cardId = self.STANDARD_CARDS['names'][str(name)]
                card = self.STANDARD_CARDS['cards'][str(cardId)]
                rarity = card['rarity']
            # if the owned quantity is less than necessary
            # add that missing amount to the missing variable
            if owned < desired:
                missing[rarity] = missing[rarity] + desired - owned
            else:
                owned = desired
            print(str(owned) + '/' + str(desired) + ' - ' + name)

        print('')
        print('Missing for ' + text + ':')

        for key, value in missing.items():
            print(' ' + key + ': ' + str(value) + '/' + str(wildcards[key]))

        print('')

    def __init__(self):
        print('Getting your collection...')
        collection = self.get_collection()
        print('Collection data acquired')
        while True:
            input('Press <Enter> when deck is in clipboard')
            print('Filtering deck...')
            dirtyDeck = self.get_deck()
            deck = self.filter_deck(dirtyDeck)
            print('Comparing against collection...')
            print('')
            self.print_data(deck, collection)
            a = input('Press <Enter> to run again or "exit" to leave\n')
            if a == 'exit':
                break


try:
    checker = DeckChecker()
except Exception as e:
    print(e)
    input()
