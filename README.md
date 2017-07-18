trumps-bigboss-bot
==================

A silly script that randomly generates tweets that make it look like
Donald Trump is actually Big Boss from the first [Metal Gear game on the
MSX](https://en.wikipedia.org/wiki/Metal_Gear_(video_game)).

This script is forked from my first proper Twitter bot, [The Jeremy
Kylebot](https://github.com/MikeCoats/kyle-bot). To learn how to fork
your own repo on GitHub, simply follow [my simple
guide](https://mikecoats.com/fork-your-own-repo/).

The quotes contained in the `patterns/big-boss.json` file were orginally
ripped by the user [Nekura_Hoka on
GameFAQs](https://www.gamefaqs.com/community/NekuraHoka), whose complete
rip can be found in the `msx--metal-gear--script.txt` file in
this repo, or on [the GameFAQs
website](https://www.gamefaqs.com/msx/578853-metal-gear/faqs/30618).

Installation
------------

* Copy the example auth file to the correct location and fill in your details.
```
cp auth/example.json auth/auth.json
$EDITOR auth/auth.json
```
* Create an empty virtual environment and work in it.
```
virtualenv .env
source .env/bin/activate
```
* Install the package requirements.
```
pip install -r requirements.txt
```

Usage
-----

* Just run the script, everything will happen automatically.
```
./trump.py
```