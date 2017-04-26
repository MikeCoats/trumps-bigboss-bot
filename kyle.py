#!/usr/bin/env python3

import json
import random
from os import listdir, path
from PIL import Image, ImageDraw, ImageFont
from twython import Twython

# We need to seed the RNG with the current time (done by not specifying
# a seed) or we'll just create the same episode again and again.
random.seed()


# A helper function returns a list of all the files in a directory.
def listfiles(filepath):
    files = []
    for f in listdir(filepath):
        if(path.isfile(path.join(filepath, f))):
            files.append(f)
    return files

# Choose a random pattern. A pattern is the form the episode title is
# written in, e.g My X Y your Z.
patterns = listfiles('patterns')
patternfile = path.join('patterns', random.choice(patterns))
# Choose a random background image
backgrounds = listfiles('backgrounds')
backgroundfile = path.join('backgrounds', random.choice(backgrounds))
# Choose a random show logo.
logos = listfiles('logos')
logofile = path.join('logos', random.choice(logos))

# Time to build the episode title.
episode = ''
with open(patternfile, 'r') as f:
    pattern = json.load(f)
    # The format will look like "{0} {1} {2} {3}." so it can be used by
    # python to build up the string.
    format = pattern['format']
    # The order specifies which list in the pattern should be used in
    # which format placeholder.
    order = pattern['order']
    # We then grab a random entry from each of the lists.
    arguments = []
    for section in order:
        data = pattern[section]
        item = random.choice(data)
        arguments.append(item)
    # And then blat the entries against the formatting string.
    episode = format.format(*arguments)

# Open the Images with Pillow as we're going to perform graphical
# operations on them.
bg = Image.open(backgroundfile)
logo = Image.open(logofile)
# Grab the image size info in sensible names. We're going to use them in
# equations later, so it'll make more sense if their names make sense.
bgwidth = bg.size[0]
bgheight = bg.size[1]
logowidth = logo.size[0]
logoheight = logo.size[1]

# We want strip across the bottom of the screen that will give us a
# little more contrast to make the episode titles easier to read.
band = Image.new('RGBA', (bgwidth, logoheight), (127, 127, 192, 127))
# We're going to draw our episode title on the band. Do some set up.
draw = ImageDraw.Draw(band)
font = ImageFont.truetype('FiraSans-Medium.ttf', 24)

# We need to offset the insert position of the episode title if it's on
# more than one line.
lines = episode.count('\n')
episodeoffset = 12
if(lines > 0):
    episodeoffset = 24
# Draw a drop-shadow, nudged over a bit.
draw.text(
    (logowidth + 2, logoheight / 2 - episodeoffset + 2), episode,
    font=font, fill=(0, 0, 0, 255))
# Draw the real text in the right place.
draw.text(
    (logowidth, logoheight / 2 - episodeoffset), episode,
    font=font, fill=(255, 255, 255, 255))

# Draw an attribution for the background images in the bottom left.
with open('attribution.json', 'r') as f:
    attributions = json.load(f)
    # Attributions use the background file's relative path as the key.
    attr = attributions[backgroundfile]
    attrfont = ImageFont.truetype('FiraSans-Regular.ttf', 8)
    draw.text(
        (0, logoheight - 8),
        'Background is derivative of “{0}” by {1} ({2}) '
        'licensed under {3}.'.format(
            attr['title'], attr['author'], attr['url'], attr['license']),
        font=attrfont, fill=(255, 255, 255, 255))

# Paste the string of colour and the logo onto the chosen background
# image.
logooffset = bgheight - logoheight
bg.paste(band, (0, logooffset), band)
bg.paste(logo, (0, logooffset), logo)
# We need to save the image to disk, as the twitter up-loader takes a
# file as its argument, not a Pillow Image. We save in 'output' as this
# is a directory git has been told about, but has also been told to
# ignore its contents.
bg.save(path.join('output', 'done.jpg'), 'JPEG')

# The authentication keys,secrets and tokens are saved in a file git
# ignores for us. Make sure you've copied the example.json file and
# filled it in according to the README.md, or you'll not be able to post
# to twitter.
with open('auth/auth.json', 'r') as f:
    file_auth = json.load(f)
    twitter = Twython(
        file_auth['app_key'], file_auth['app_secret'],
        file_auth['oauth_token'], file_auth['oauth_token_secret'])
    auth = twitter.get_authentication_tokens()
    # The mode here must be 'rb' and not just 'r' or the utf-8 decoder
    # will throw a tantrum.
    image_open = open(path.join('output', 'done.jpg'), 'rb')
    # Posting an image status is a two-part job.
    # 1. Upload the image
    image_ids = twitter.upload_media(media=image_open)
    # 2. Make a status update that references the media id.
    twitter.update_status(
        status='Coming up: ' + episode + ' #jeremykyle',
        media_ids=image_ids['media_id'])
