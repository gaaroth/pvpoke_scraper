# SETUP

## Virtualenv
Run these commands to prepare the project
Assuming you have a python3.6 installed and working with virtualenvs

```bash
mkvirtualenv  -a  . -p $(which python3.6) pvpoke-scraper
workon .
pip install -r requirements.txt
pip install ipdb
pip install -e .
```

## Install required stuff for selenium
```bash
brew install geckodriver
```


# RUN THE SCRIPT
```bash
python ./src/scraper.py 
```


# NOTES

## Intro
This is just a simple script laid down in a couple of hours of work and tries.
It still can be hugely improved. If you have ideas or suggestion feel free to make a pull requests or contact me.

## Results
After you run the script a result_csv.csv file is created. I like to import it in a google spreadsheet file and add some formatting to look better.

## Move
If you need to update or check the moves look into src/poke_dictionary.py
Unfortunately, for now, I've saved just the indexes of the moves for their relative Pokemon, but the index can change with moves updates (since PvPoke show them alphabetically ordered).
I'm planning to add the move codenames instead but that will require to make 2 calls, 1 to get the current move index e another to get the actual sim.
In any case, just double-check in the finals CSV if the moves are the expected ones and eventually fix the poke_dictionary.
Feel free to make a pull request for these fixes or to add more Pokemon, I've just added the ones I'm currently testing.

## Movesets
To handle different movesets, there's a duplicate entry in the poke_dictionary with a tailing number, remember to match the correct name in your attacker or defender pokemon lists.