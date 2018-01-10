# bot-joi
A random Discord bot for silly stuff.

In order to run the audio parts of this bot, you need to install FFMPEG which can be found at https://www.ffmpeg.org/. 

Other dependencies:
- bs4 BeautifulSoup (py -m pip install BeautifulSoup4)
- Rapptz/discord.py (py -m pip install -U discord.py[voice])
- Requests (py -m pip install requests)
- Giphy_client (py -m pip install giphy_client)
- billy-yoyo/RainbowSixSiege-Python-API (py -m install r6sapi)

Current features:  
- Reacts to certain phrases and words with emojis and replies
- Can join and disconnect from voice serves in order to play sounds
- Do dice simulations

List of commands: (to call the bot, start your message with 'joi, ')
- help - display commands
- var *user* - Returns a cheecky answer depending on the current user status
- hej - Say hello to the bot
- kom, här - Get bot to enter your current voice channel
- sov, stick - Get bot to exit your current voice channel
- play *sound* - If not already in your current voice channel, go to that channel before playing the input sound
- roll *dice* - Rolls a dice simulation, e.g. "joi, roll 4d6 1d8"
- wiki me, reddit me *article/subreddit* - Returns a link to that subreddit or wikipedia article. 
- news - Returns some news article headers.
- r6 <kills, deaths, kd, playtime, record, win, mystats>  - Returns some stats from R6.
- joke - returns a joke from r/jokes

Current sounds and alias: 
- Sad Drumroll - drum
- Saleel Sawarim - isis
- DUN DUN - dun
- Sad Trombone - sad
- Haha - haha
- Split up - clues

TODO: Add more features, add more sounds, maybe add fuzzy search, update code to match PEP8 style guide
