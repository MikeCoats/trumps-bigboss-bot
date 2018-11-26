#!/usr/bin/env python3

import json
import random
from os import listdir, path
from PIL import Image, ImageDraw, ImageFont
from twython import Twython

# We need to seed the RNG with the current time (done by not specifying
# a seed) or we'll just use the same quote again and again.
random.seed()

# A helper function returns a list of all the files in a directory.
def listfiles(filepath):
    files = []
    for f in listdir(filepath):
        if(path.isfile(path.join(filepath, f))):
            files.append(f)
    return files

# Choose the pattern file
patterns = listfiles('patterns')
patternfile = path.join('patterns', random.choice(patterns))
# Choose a random background image
backgrounds = listfiles('backgrounds')
backgroundfile = path.join('backgrounds', random.choice(backgrounds))

# Time to build the tweet.
his_tweet = []
our_tweet = ''
our_hashtags = []

with open(patternfile, 'r') as f:
    pattern = json.load(f)

    # His tweet is the one that will be in the screenshot.
    his_tweet = random.choice(pattern['his_lines'])

    # Our tweet is the message of shock we're displaying.
    our_tweet = random.choice(pattern['our_tweets'])

    # The hashtags are for our tweets.
    hashtags = pattern['hashtags']
    tag1 = random.choice(hashtags)
    hashtags.remove(tag1)
    tag2 = random.choice(hashtags)
    hashtags.remove(tag2)
    tag3 = random.choice(hashtags)

    our_hashtags.append(tag1)
    our_hashtags.append(tag2)
    our_hashtags.append(tag3)

# This is all the tweet screenshot layout information we need.
tweet_top = 80
tweet_left = 20
timestamp_top = 210
timestamp_left = tweet_left
retweets_top = 252
retweets_left = tweet_left+10
likes_top = retweets_top
likes_left = 144

rp_top = 291
rp_left = 50
rt_top = rp_top
rt_left = 130
ht_top = rp_top
ht_left = 210


# This is for the tweet engagement scores.
replies = random.randint(13000,54000)
retweets = random.randint(15000,31000)
likes = random.randint(55000,99000)

retweets_s = "{0}".format(retweets)
likes_s = "{0}".format(likes)

rp = "{0}K".format(int(replies / 1000))
rt = "{0}K".format(int(retweets / 1000))
ht = "{0}K".format(int(likes / 1000))


# Use Pillow to draw on our chosen background image.
bg = Image.open(backgroundfile)
draw = ImageDraw.Draw(bg)

# Load the fonts for the body & the engagements.
body_font = ImageFont.truetype('FiraSans-Medium.ttf', 24)
small_font = ImageFont.truetype('FiraSans-Regular.ttf',14)

# Do a little vertical centring - this is not correct, but it's close.
lineoffset = 30
tweet_offset = ((4-len(his_tweet)) * lineoffset) / 2
tweet_top = tweet_top + tweet_offset

# Write out the tweet.
for i in range(len(his_tweet)):
    draw.text((tweet_left,tweet_top+i*lineoffset),his_tweet[i],font=body_font, fill=(0,0,0,255))

# Write out the engagement scores
draw.text((retweets_left,retweets_top),retweets_s,font=small_font, fill=(0,0,0,255))
draw.text((likes_left,likes_top),likes_s,font=small_font, fill=(0,0,0,255))

draw.text((rp_left,rp_top),rp,font=small_font, fill=(96,96,96,255))
draw.text((rt_left,rt_top),rt,font=small_font, fill=(96,96,96,255))
draw.text((ht_left,ht_top),ht,font=small_font, fill=(96,96,96,255))

# Save the image to disk as the twython api uses files for posting.
bg = bg.convert('RGB')
bg.save(path.join('output', 'done.jpg'), 'JPEG')

# Make up a fake tweet ID so that it looks like it's been deleted.
tweet_id = random.randint(100000000000000000,999999999999999999)

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
        status='{0} {1} {2} {3} https://twitter.com/realDonaldTrump/status/{4}'.format(our_tweet, our_hashtags[0], our_hashtags[1], our_hashtags[2], tweet_id),
        media_ids=image_ids['media_id'])
