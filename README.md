# bot-joi
A random Discord bot for silly stuff.

In order to run the audio parts of this bot, you need to install FFMPEG which can be found at https://www.ffmpeg.org/. 

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

Current sounds and alias: 
- Sad Drumroll - drum
- Saleel Sawarim - isis

TODO: Add more features, add more sounds, maybe add fuzzy search, update code to match PEP8 style guide
