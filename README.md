kyle-bot
========

A silly script that randomly generates Jeremy Kyle episodes and posts
them to twitter.

Installation
------------

* Copy the example auth file to the correct location and fill in your details.
```
cp auth/example.json auth/auth.json
$EDITOR auth/auth.json
```
* Create an empty virtual environment .
```
virtualenv .
```
* Install the package requirements.
```
pip install -r requirements.txt
```

Usage
-----

* Just run the script, everything will happen automatically.
```
./kyle.py
```