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

> P.S. Those must be run in the same folder as the Pipfile

If you want to make it an executable, run:

```
pipenv run pyinstaller -F deck_check.py
// The output .exe file will be in a folder called dist
// Then all you have to do is copy/paste the cards.json file into the /dist folder. 
```


Example run with deck using format accepted by "MTG: Arena":

```
Getting your collection...
Collection data acquired
Press <Enter> when deck is in clipboard
Filtering deck...
Comparing against collection...

0/1 - Fanatical Firebrand
19/19 - Mountain
0/4 - Spear Spewer
3/4 - Ghitu Lavarunner
2/4 - Viashino Pyromancer
0/4 - Electrostatic Field
4/4 - Shock
4/4 - Lightning Strike
1/4 - Wizard's Lightning
0/4 - Risk Factor
0/4 - Light Up the Stage
0/4 - Skewer the Critics

Missing for main deck (nr missing / nr wildcards owned):
 common: 12/5
 uncommon: 11/9
 rare: 4/4
 mythic: 0/4

Press <Enter> to run again or "exit" to leave
```
