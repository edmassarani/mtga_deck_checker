from mtga.set_data import all_mtga_cards
from mtga import set_data
import win32clipboard
import os
import re


class DeckChecker:
    # keyword for getting collection from log
    KEYWORD = "PlayerInventory.GetPlayerCardsV3"

    # log's location on the computer
    LOG_LOCATION = os.getenv(
        'APPDATA') + "\\..\\LocalLow\\Wizards Of The Coast\\MTGA\\output_log.txt"

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
                card = all_mtga_cards.find_one(cardId)
                quantity = int(line[9])
                collection[card.pretty_name] = [quantity, card]
            if line.find('}') > -1:
                start = False

        return collection

    def get_deck(self):
        # get the desired deck from the clipboard
        win32clipboard.OpenClipboard()
        clipboard = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()

        # split the data into a list
        dirtyDeck = clipboard.split('\r\n')

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
        mainDeck = {}
        sideBoard = {}

        # loop through each card and save them if they are valid
        for card in dirtyDeck[0]:
            if not re.match(r'\d{1,2} .* \([A-Z0-9]{3}\) .*', card):
                print('Invalid deck')
                print('(' + card + ')\nIs not a card')
                exit()
            card = card.split(' ')
            quantity = int(card[0])
            for idx, val in enumerate(card):
                if re.match(r'\([A-Z0-9]{3}\)', val):
                    stopName = idx
                    break
            name = ' '.join(card[1:stopName])
            mainDeck[name] = quantity

        if dirtyDeck[1]:
            for card in dirtyDeck[1]:
                if not re.match(r'\d{1,2} .* \([A-Z0-9]{3}\) .*', card):
                    print('Invalid deck')
                    print('(' + card + ')\nIs not a card')
                    exit()
                card = card.split(' ')
                quantity = int(card[0])
                for idx, val in enumerate(card):
                    if re.match(r'\([A-Z0-9]{3}\)', val):
                        stopName = idx
                        break
                name = ' '.join(card[1:stopName])
                sideBoard[name] = quantity

        return [mainDeck, sideBoard]

    def print_data(self, deck, collection):
        # variable for counting the missing rarities
        missingMain = {
            "Common": 0,
            "Uncommon": 0,
            "Rare": 0,
            "Mythic Rare": 0,
        }
        missingSide = {
            "Common": 0,
            "Uncommon": 0,
            "Rare": 0,
            "Mythic Rare": 0,
        }

        # loop through each card in the main deck
        for name, desired in deck[0].items():
            # check if they exist in the colection or if it's a basic land
            # get the owned quantity of the card
            if name in collection:
                data = collection.get(name)
                owned = data[0]
                card = data[1]
                rarity = card.rarity
            elif name in ['Mountain', 'Forest', 'Plains', 'Island', 'Swamp']:
                owned = desired
            else:
                owned = 0
                card = set_data.all_mtga_cards.search(
                    name.replace(' ', '_'), True)[0]
                rarity = card.rarity
            # if the owned quantity is less than necessary
            # add that missing amount to the missing variable
            if owned < desired:
                missingMain[rarity] = missingMain[rarity] + desired - owned
            else:
                owned = desired
            print(str(owned) + '/' + str(desired) + ' - ' + name)

        if deck[1]:
            print('')
            # loop through each card in the sideboard
            for name, desired in deck[1].items():
                # check if they exist in the colection or if it's a basic land
                # get the owned quantity of the card
                if name in collection:
                    data = collection.get(name)
                    owned = data[0]
                    card = data[1]
                    rarity = card.rarity
                elif name in ['Mountain', 'Forest', 'Plains', 'Island', 'Swamp']:
                    owned = desired
                else:
                    owned = 0
                    card = set_data.all_mtga_cards.search(
                        name.replace(' ', '_'), True)[0]
                    rarity = card.rarity
                # if the owned quantity is less than necessary
                # add that missing amount to the missing variable
                if owned < desired:
                    missingSide[rarity] = missingSide[rarity] + desired - owned
                else:
                    owned = desired
                print(str(owned) + '/' + str(desired) + ' - ' + name)

        print('')
        print('Missing for main deck')

        for key, value in missingMain.items():
            print(' ' + key + ': ' + str(value))

        if deck[1]:
            print('')
            print('Missing for side board')

            for key, value in missingSide.items():
                print(' ' + key + ': ' + str(value))

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


checker = DeckChecker()
