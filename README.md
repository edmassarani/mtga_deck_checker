# MTGA Deck Checker

A simple python command line program to get your MTG: Arena collection from the log files and check a deck against it.

You must have python and pipenv installed.

```
python --version
// Python 3.7.2
```

```
pip install pipenv
```

After installing both, you must then install all the project dependencies by running this in the folder where the Pipfile is saved

```
pipenv install
```

To run the program in the command line you then simply need to run:

```
pipenv run python deck_check.py
```

If you want to make it an executable, run:

```
pipenv run pyinstaller --onefile deck_check.py
// The output .exe file will be in a folder called dist
```


Example run with deck copied from MTGGoldfish's export to Magic Arena:

```
Getting your collection...
Collection data acquired ✔
<Press enter when deck is in clipboard>
Filtering deck...
Comparing against collection...

4/4 - Merfolk Trickster
4/4 - Mist-Cloaked Herald
4/4 - Siren Stormtamer
4/4 - Tempest Djinn
3/4 - Warkite Marauder
1/1 - Chart a Course
4/4 - Dive Down
0/1 - Lookout's Dispersal
3/4 - Opt
2/2 - Spell Pierce
4/4 - Wizard's Retort
4/4 - Curious Obsession
20/20 - Island

1/1 - Chart a Course
1/1 - Spell Pierce
1/1 - Disdainful Stroke
1/1 - Entrancing Melody
2/2 - Essence Scatter
2/2 - Exclusion Mage
0/1 - Negate
2/2 - Sleep
0/2 - Surge Mare
1/2 - Transmogrifying Wand

Missing for main deck
 Common: 1
 Uncommon: 1
 Rare: 1
 Mythic Rare: 0

Missing for side board
 Common: 1
 Uncommon: 2
 Rare: 1
 Mythic Rare: 0
 ```
