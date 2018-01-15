import discord
import asyncio
import random
import time
import operator
import threading
import r6sapi
import json
import giphy_client
import requests
import json
from giphy_client.rest import ApiException
import urllib.request as urlRequest
import urllib.parse as urlParse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from discord.ext import commands



if not discord.opus.is_loaded():
	# the 'opus' library here is opus.dll on windows
	# or libopus.so on linux in the current directory
	# you should replace this with the location the
	# opus library is located in and with the proper filename.
	# note that on windows this DLL is automatically provided for you
	discord.opus.load_opus('opus')

gejmArr = ['Hörde jag gejm?', 'Yay for gejm!', 'Nu är det dags', 'PUBG?','Siege?','Golf with your Friends?', 'CS?', 'Worms?', 'Deceit?'];
hereArr = [' ska vara här', ' är här... nånstans :3', ' bör vara här', ' lovade att skulle vara gejm snart :)']
awayAnswers = [' är inte här i alla fall', ' lagar mat eller nått', ' kommer nog snart hoppas jag', ' verkar vara AFK :/'];
goneBeginAnswers = ['Jag har inte sett ', 'Jag har inte hört från '];
goneEndAnswers = [' på ett tag. Sorri :3', ' på en stund.', ' på evigheter... Suck.'];
deleteArr = ['Jag såg dig allt ;)', 'Vad försökte du dölja nu?', 'I remember all', 'Jag kan hålla en hemlighet']
wowArr = ['Det suger...', 'Det är bara töntar som spelar WoW.' ,'2004 ringde. De vill ha tillbaka sitt spel.', 'Saker jag hellre skulle göra än att spela WoW: dränka kattungar', 'Wow? Hörde att Viktor spelar på RP-servrar', "WoW? Det är som Runescape va? Fast sämre?"];
welcomeArr = ['Hej hej ', 'Tjo ', 'Hallå ', 'Hejsan ', 'Tja ']
sleepArr = ['Jag sover redan, stör mig inte :<', 'Zzzzzz', '*gäsp* vad vill du ens?'];
joiArr = ['Pratar ni om mig?', 'Hörde jag mitt namn?', 'Here to serve :)', ':notes: You know my name, you know my name :musical_note:', 'Hej hej', 'Vad kan jag stå till tjänst med idag?', ":o"];
dogeArr = ['doge', 'doge2']
teamArr = ['Klart!', 'Är det dags att visa vem som bestämmer?', 'Lite rivalitet har ingen dött av.', 'Lycka till!', 'Må bästa laget vinna :D', 'Lova att inte bråka för mycket nu :3']
bladrunnerArr = ['Do you like our owl?', 'Is this testing whether I\'m a Replicant or a lesbian, Mr. Deckard?', 'Replicants are like any other machine. They\'re either a benefit or a hazard. If they\'re a benefit, it\'s not my problem.', 'Nothing is worse than having an itch you can never scratch.', 'I\'ve seen things you people wouldn\'t believe', 'All those ... moments will be lost in time, like tears...in rain.', ' Sometimes to love someone, you got to be a stranger.', '4 symbols make a man: A, T, G & C. I am only two: 1 and 0.', 'You look like a *good* Joe.',  'I\'ve never seen a tree. It\'s pretty.'];
foodArr = ['\U0001F35E', '\U0001F356', '\U0001F9C0', '\U0001F357', '\U0001F953', '\U0001F354', '\U0001F355', '\U0001F32E', '\U0001F32F', '\U0001F959', '\U0001F373', '\U0001F958', '\U0001F372', '\U0001F957', '\U0001F371', '\U0001F375'];

soundDict = {
    'drum' : 'joke_drum_effect.mp3',
    'isis' : 'Saleel_Sawarim.mp3',
    'sad' : 'sadtrombone.mp3',
    'haha' : 'haha.mp3',
    'dun' : 'DUN_DUN.mp3',
    'clues' : 'clues.mp3',
    'clue' : 'clues.mp3',
    'x-files' : 'x-files.mp3',
    'spaghet' : 'spaghet.mp3',
    'spaghett' : 'spaghet.mp3',
    'spaget' : 'spaghet.mp3',
}
ubiDict = {
    '246342885853626369' : 'Beasterino',
    '246357307661746176' : 'DameValerie',
    '185110609216405504' : 'Netstroyer',
    '246362414436712449' : 'hjortronhatt',
    '246343288422924288' : 'KaptenStjert',
    '114389410069479424' : 'Pooze',
    '169075098257457152' : 'ThaC0w'
}
global server
global localVoiceClient
localVoiceClient = None
global lock
lock = False

async def joi_test(message, client):  
    # tmp = await client.send_message(message.channel, 'Räknar meddelanden...')
    # counter = 0
    # async for log in client.logs_from(message.channel, limit=100):
    #     if log.author == message.author:
    #         counter += 1
    # await client.edit_message(tmp, 'Du har skrivit {} meddelanden senaste sessionen.'.format(counter))
    reply = ''
    i = 1
    for e in foodArr:
        reply += str(i) + ': ' + e + ' '
        i += 1
    await client.send_message(message.channel, reply)

async def joi_hello(message, client): 
    reply = random.choice(welcomeArr) + message.author.name
    await client.send_message(message.channel, reply)

async def joi_wow(message, client): 
    reply = random.choice(wowArr)
    await client.send_message(message.channel, reply)

async def joi_find(message, client):  
    if len(message.mentions) == 0:
        await client.send_message(message.channel, 'Vem sade du?')
    for user in message.mentions:
        if user.status == discord.Status.idle or user.status == discord.Status.dnd:
            reply = user.name +  random.choice(awayAnswers)
        elif user.status == discord.Status.offline:
            reply = random.choice(goneBeginAnswers) + user.name + random.choice(goneEndAnswers)
        elif user.status == discord.Status.online:
            reply = user.name + ' ska vara här'    
        await client.send_message(message.channel, reply)

async def joi_come(message, client):
    global localVoiceClient
    if localVoiceClient is not None:
        await localVoiceClient.disconnect()
    localVoiceClient = await client.join_voice_channel(message.author.voice.voice_channel)

async def joi_sleep(message, client):
    global localVoiceClient
    if localVoiceClient is not None:
        await localVoiceClient.disconnect()
        localVoiceClient = None
    else:
        reply = random.choice(sleepArr)
        await client.send_message(message.channel, reply)

async def joi_play(message, client):
    sound = soundDict.get(message.content.split(' ')[1])
    global localVoiceClient
    global server
    callUser = discord.utils.find(lambda m: m.id == message.author.id, server.members)
    if callUser.voice.voice_channel is None:
        await client.send_message(message.channel, 'Du sitter ju inte ens i en röstkanal :/')
        return
    if hasattr(localVoiceClient, 'channel'):
        if localVoiceClient.channel != message.author.voice.voice_channel:
            await joi_come(message, client)
    else:
        await joi_come(message, client)
    player = localVoiceClient.create_ffmpeg_player('sounds/' + sound)
    player.start()

async def joi_dice(message, client):
    dice = message.content[6:]
    dice = dice.split(' ')
    result = []
    reply = ''
    rollSum = 0
    for roll in dice:
        roll = roll.split('d')
        ctr = int(roll[0])
        if ctr > 100:
            await client.send_message(message.channel, 'Haha... Kul... Du vet vad jag gillar när man försöker krasha mig >:(')
            return
        while ctr > 0:
            result.append(random.randint(1, int(roll[1])))
            ctr -= 1
    for e in result:
        rollSum += e 
        reply += str(e) + ', '
    if len(reply) < 250:
        await client.send_message(message.channel, 'Du rullade ' + reply +  'vilket ger en summa av ' + str(rollSum))
    else:
        await client.send_message(message.channel, 'Försökte du precis krasha mig? :< I alla fall, summan blev ' + str(rollSum))

async def joi_wiki(message, client):
    reply = 'https://en.wikipedia.org/wiki/' + message.content.split(' ')[2]
    await client.send_message(message.channel, 'Varsågod: ' + reply)

async def joi_reddit(message, client):
    reply = 'https://www.reddit.com/r/' + message.content.split(' ')[2]
    await client.send_message(message.channel, 'Här: ' + reply)

async def joi_help(message, client):
    with open('help.txt', 'r') as f:
        help_text = f.read()
    await client.send_message(message.channel, 'Här: ' + help_text)

async def joi_scrape_news(message, client):
    data = []
    articles = []
    quote_page = ['https://www.expressen.se/', 'https://www.aftonbladet.se/', 'https://www.dn.se/', 'https://www.svd.se/']
    for pg in quote_page:
        page = urlopen(pg)
        soup = BeautifulSoup(page, 'html.parser')
        title_div = soup.find_all(['h2', 'h3'])
        for hd in title_div:
            article = hd.get_text()
            if len(article) > 15:
                data.append(article)
                break
    reply = 'Senaste nytt: \n**SvD**: ' + data.pop() + '\n**DN**: ' + data.pop() + '\n**Aftonbladet:** ' + data.pop() + '\n**Expressen:** ' + data.pop()
    await client.send_message(message.channel, reply)


async def get_kills(player):
    return player.ranked.kills

async def get_deaths(player):
    return player.ranked.deaths

async def get_revives(player):
    return player.revives

async def get_melee(player):
    return player.melee_kills

async def get_assists(player):
    return player.kill_assists

async def get_kd(player):
    return round((player.ranked.kills / player.ranked.deaths), 3) 

async def get_playtime(player):
    return str(round((player.ranked.time_played/3600), 2)) + 'h'

async def get_record(player):
    return str(player.ranked.won) +' - ' + str(player.ranked.lost)

async def get_win(player):
    return str(round((player.ranked.won/player.ranked.played)*100, 3)) + '%'

def kd_calculator(kills, deaths):
    if deaths != 0:
        return kills/deaths 
    else:
        return 0

async def get_favop(player, retriever = lambda p : p.time_played, converter = lambda p: str(round((p/3600), 2)) + 'h'):
    await player.load_all_operators()
    most_played = max(player.operators.values(), key = retriever)
    return most_played.name.capitalize() +' (' + str(converter(retriever(most_played))) +')'

async def joi_r6_stats(message, client):

    r6statDict = {
    'kills' : get_kills,
    'deaths' : get_deaths,
    'assists' : get_assists,
    'revives' : get_revives,
    'melee' : get_melee,
    'kd' : get_kd,
    'playtime' : get_playtime,
    'record' : get_record,
    'win' :  get_win,
    'favop' : get_favop
    }

    parameterDictionary = {
    'playtime' : [lambda p : p.time_played, lambda p: str(round((p/3600), 2)) + 'h'],
    'kills' : [lambda p : p.kills, lambda p : p],
    'deaths' : [lambda p : p.deaths, lambda p: p],
    'melee' : [lambda p : p.melees, lambda p : p],
    'wins' :  [lambda p :  p.wins, lambda p : p],
    'losses' : [lambda p: p.losses, lambda p : p],
    'kd' : [lambda p : kd_calculator(p.kills, p.deaths), lambda p: str(round(p, 3))]
    }

    reply = ''
    result_list = []
    stat_type = message.content.split(' ')[1]

    #Read credentials and players from external documents
    with open('keys/uplaycred.txt', 'r') as f:
        credentials = f.readlines()
    credentials = [x.strip() for x in credentials] 
    with open('players.txt', 'r') as f:
        player_names = f.readlines()
    player_names = [x.strip() for x in player_names] 

    if len(message.content.split(' ')) == 3:
        second_paramter = message.content.split(' ')[2]
    else:
        second_paramter = ''

    auth = r6sapi.Auth(credentials[0], credentials[1])

    #Get stats based on type
    if stat_type != 'mystats' and stat_type != None:
        stat_func = r6statDict.get(stat_type)
        if stat_func == None:
            await client.send_message(message.channel, 'Vad ville du veta sade du? Prova kills, deaths, assists, revives, melee, kd, playtime, record, win, favop eller istället. :) ')
            await auth.session.close()
            return
        for player in player_names:
            acc = await auth.get_player(player, r6sapi.Platforms.UPLAY)
            await acc.load_queues()
            await acc.load_general()
            if stat_type == 'favop':
                funcs = parameterDictionary.get(second_paramter, parameterDictionary.get('playtime'))
                retriever = funcs[0]
                converter = funcs[1]
                result_list.append((player, await get_favop(acc, retriever, converter)))
            else:
                result_list.append((player, await stat_func(acc)))

        result_list.sort(key=operator.itemgetter(1), reverse = True)
    else:
        player = ubiDict.get(message.author.id)
        acc = await auth.get_player(player, r6sapi.Platforms.UPLAY)
        await acc.load_queues()
        await acc.load_general()
        if second_paramter == '':
            for key, value in r6statDict.items():
                result_list.append((key.capitalize(), await value(acc)))
        else:
            await acc.load_all_operators()
            p_operator = acc.operators.get(second_paramter)
            if p_operator == None:
                await auth.session.close()
                await client.send_message(message.channel, 'Det fanns ingen operator som hette sådär hörredu.')
                return
            for key, value in parameterDictionary.items():
                result_list.append((key.capitalize(), str(value[1](value[0](p_operator)))))
            result_list.append((p_operator.statistic_name, str(p_operator.statistic)))

    #Create and return reply
    reply = 'Jag hörde att du ville ha lite statistik ' + '[ ' + stat_type.capitalize() + ' ' + second_paramter.capitalize() + ' ] :\n'     
    for stat in result_list:
        reply = reply + stat[0] + ' - ' + str(stat[1]) + '\n'
    
    await auth.session.close()
    await client.send_message(message.channel, reply)
    return

async def joi_scrape_joke(message, client):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    joke = []
    reply = ''
    long_joke = True
    #get a random joke from FP
    page = 'https://www.reddit.com/r/Jokes/'
    req = urlRequest.Request(page, headers = headers)
    url = urlRequest.urlopen(req)
    sourceCode = url.read()
    soup = BeautifulSoup(sourceCode, 'html.parser')
    title = soup.find_all('p', attrs={'class': 'title'})
    title.pop(0)
    #Choose one joke that is not tagged as long
    while (long_joke):
        post = random.choice(title)
        flair = post.find('span', attrs={'title': 'Long'})
        if (flair == None):
            long_joke = False

    post = post.find('a', attrs={'class': 'title'})
    post = post.get('href')

    #Go to joke page
    page = 'https://www.reddit.com' + post
    req = urlRequest.Request(page, headers = headers)
    url = urlRequest.urlopen(req)
    sourceCode = url.read()
    soup = BeautifulSoup(sourceCode, 'html.parser')

    #Grab header
    joke_start = soup.find('p', attrs={'class': 'title'}).find('a', { "class" : "title" },recursive=False).text.strip()
    joke.append(joke_start)
    #Grab rest
    joke_rest = soup.find('div', attrs={'class': 'expando'}).find_all('p')
    for line in joke_rest:
        line = line.text.replace('</p>', '')
        line = line.replace('<p>', '')
        joke.append(line)
    for line in joke:
        reply = reply + line + '\n'
    await client.send_message(message.channel, reply)

async def joi_daily_deal(message, client):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    joke = []
    reply = ''
    page = 'http://store.steampowered.com/?l=swedish'

    req = urlRequest.Request(page, headers = headers)
    url = urlRequest.urlopen(req)
    sourceCode = url.read()
    soup = BeautifulSoup(sourceCode, 'html.parser')
    daily_deal = soup.find('a', attrs={'class': 'daily_deal'})
    daily_deal = daily_deal.get('href')

    reply = 'Dagens deal på steam är: \n' + daily_deal
    await client.send_message(message.channel, reply)

async def joi_teams(message, client):
    current_vc = discord.utils.find(lambda m: m.id == message.author.id, server.members).voice.voice_channel
    new_team_vc = None
    number_of_players = len(current_vc.voice_members)
    new_team_text = []
    team1 = ''
    team2 = ''
    if number_of_players % 2 != 0:
        await client.send_message(message.channel, 'Men ni är ju inte ett jämnt antal :<')
        return
    for ch in server.channels:
        if ch.type == discord.ChannelType.voice and ch.voice_members == []:
            new_team_vc = ch
            break
    halved = number_of_players/2
    members_copy = current_vc.voice_members.copy()

    while (number_of_players != halved):
        mem_to_move = members_copy.pop(random.randint(0, number_of_players-1))
        new_team_text.append(mem_to_move)
        #await client.move_member(mem_to_move, new_team_vc)
        number_of_players = number_of_players-1
    for mem in members_copy:
        team1 = team1 + mem.name + '\n'
    for mem in new_team_text:
        team2 = team2 + mem.name + '\n'
    #await client.send_message(message.channel, random.choice(teamArr))
    reply = '**Lag 1: **\n' + team1 + '**Lag 2: **\n' + team2 + '\n\n' + random.choice(teamArr)
    await client.send_message(message.channel, reply)

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

async def joi_giphy(message, client): 
    search_string = message.content[4:]

    if is_number(search_string[-1:]):
        r = int(search_string[-1:])
        search_string = search_string[:-2]
    else:
        r = random.randint(0, 2)

    if len(search_string) > 0:
        query = search_string # str | Search query term or prhase.
    else:
        await client.send_message(message.channel, 'Vad vill du ha en gif på?')
        return

    # create an instance of the API class
    api_instance = giphy_client.DefaultApi()
    api_key = 'dc6zaTOxFJmzC' # str | Giphy API Key.
    limit = 25 # int | The maximum number of records to return. (optional) (default to 25)
    offset = 0 # int | An optional results offset. Defaults to 0. (optional) (default to 0)
    rating = 'g' # str | Filters results by specified rating. (optional)
    lang = 'en' # str | Specify default country for regional content; use a 2-letter ISO 639-1 country code. See list of supported languages <a href = \"../language-support\">here</a>. (optional)
    fmt = 'json' # str | Used to indicate the expected response format. Default is Json. (optional) (default to json)

    try: 
        # Search Endpoint
        api_response = api_instance.gifs_search_get(api_key, query, limit=limit, offset=offset, rating=rating, lang=lang, fmt=fmt)
        gif_images = api_response.data.pop(r)
    except Exception as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)
        await client.send_message(message.channel, 'Oooops. Nått gick snett på andra sidan. Gifen du letade efter kanske inte fanns :<')
        return

    await client.send_message(message.channel, gif_images.embed_url)

async def joi_hearthstone(message, client): 
    input = message.content[3:]

    if input[0:3] == 'sök' or input[0:6] == 'search':
        card = input.split(' ')[1]
        endpoint = 'https://omgvamp-hearthstone-v1.p.mashape.com/cards/search/'
        search = True
    else:
        card = input
        endpoint = 'https://omgvamp-hearthstone-v1.p.mashape.com/cards/'
        search = False

    if card == '':
        await client.send_message(message.channel, 'Vilket kort letade du efter sade du?')
        return

    with open('keys/hskey.txt', 'r') as f:
        key = f.readline()

    req = requests.get(endpoint + card, headers={"X-Mashape-Key": key, "Accept": "application/json"})
    card_url = req.json()

    try:
        if search:
            reply = 'Jag hittade följande kort: \n'
            for _, element in zip(range(10), card_url):
               reply += element.get('name') + '\n'
            if len(card_url) > 10:
                reply += 'plus ' + str((len(card_url)) - 10) + ' andra kort'
        else:
            reply = card_url[-1].get('img')
    except Exception as e:
        print("Exception when calling DefaultApi->card_search_get: %s\n" % e)
        await client.send_message(message.channel, 'Oooops. Jag hittade inget som hette så.')
        return

    await client.send_message(message.channel, reply)

async def joi_klunsa(message, client):
    moves = {
    'sten': 'sax',
    'sax' : 'påse',
    'påse' : 'sten'
    }
    user_move = message.content
    joi_move = random.choice(list(moves.keys()))
    
    if moves.get(user_move) == joi_move:
        reply = joi_move.capitalize() + '! Du vinner :)' 
    elif moves.get(joi_move) == user_move:
        reply = joi_move.capitalize() + '! Jag vinner :)' 
    elif joi_move == user_move:
        reply = joi_move.capitalize() + '! Det blev visst lika' 
    else: 
        reply = 'Jag tror inte det där var ett giltligt drag :/'

    await client.send_message(message.channel, reply) 

async def joi_secret(message, client):
    in_data = message.content.split(' ')

    with open('secrets.txt', 'r') as f:
        quotes = f.read().splitlines()
    
    if len(in_data) == 2:
        temp = []
        for e in quotes:
            if in_data[1] in e:
                temp.append(e)
        quotes = temp

    try:
        reply = random.choice(quotes)
    except Exception as e:
        reply = 'Det fanns inga hemlighet här inte :3'
    await client.send_message(message.channel, reply) 

responseDict = {
    'test' : joi_test,
    'var' : joi_find,
    'hej': joi_hello,
    'wow' : joi_wow,
    'kom' : joi_come,
    'här' : joi_come,
    'sov' : joi_sleep,
    'stick' : joi_sleep,
    'dra' : joi_sleep,
    'play' : joi_play,
    'rulla' : joi_dice,
    'roll' : joi_dice,
    'wiki' : joi_wiki,
    'reddit' : joi_reddit,
    'help' : joi_help,
    'halp' : joi_help,
    'hjälp' : joi_help,
    'news' : joi_scrape_news,
    'nyheter' : joi_scrape_news,
    'r6' : joi_r6_stats,
    'lag' : joi_teams,
    'teams' : joi_teams,
    'joke' : joi_scrape_joke,
    'gif' : joi_giphy,
    'hs' : joi_hearthstone,
    'sax' : joi_klunsa,
    'påse' : joi_klunsa,
    'sten' : joi_klunsa,
    'dd' : joi_daily_deal,
    'secret' : joi_secret,
    'hemlighet' : joi_secret

}

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    global server
    server = discord.utils.find(lambda s: s.id == '246343097611583488', client.servers)
    print(server)
    print('------')

@client.event
async def on_message(message):
    global lock
    if lock: 
        return

    lock = True
    message.content = message.content.lower()
    randMess = random.randint(0, 7)

    if message.content.find('game') > -1 and randMess == 1:
        reply = random.choice(gejmArr)
        await client.send_message(message.channel, reply)

    elif message.content.find('doge') > -1 or message.content.find('shiba') > -1 or message.content.find('hund ') > -1:
        emoji = random.choice(dogeArr)
        await client.add_reaction(message, discord.utils.find(lambda e: e.name == emoji, client.get_all_emojis()))

    elif message.content.find(' mat ') > -1 or message.content.find('middag') > -1 or message.content.find('lunch') > -1 or message.content.find('äter') > -1:
        emoji = random.choice(foodArr)
        print(str(emoji))
        await client.add_reaction(message, emoji)

    elif message.content.find('bladerunner') > -1:
        reply = random.choice(bladrunnerArr)
        await client.send_message(message.channel, reply)

    elif message.content.find('tarotkort') > -1:
        await client.send_message(message.channel, "Brädspel*")

    elif message.content.startswith('joi,'):
        global localVoiceClient

        message.content = message.content[5:]
        inputMsg = message.content.split(' ')

        response = responseDict.get(inputMsg[0])

        if response is not None:
        	await response(message, client)
        elif randMess == 4:
            await client.send_message(message.channel, 'Det verkar som du ville mig något, men jag förstod inte riktigt. Du kan alltid prova att skriva help :)')

    elif message.content.find('joi') > -1 and message.author.id != '386139218885476352' and randMess == 1:
        reply = random.choice(joiArr)
        await client.send_message(message.channel, reply)
    lock = False

@client.event
async def on_message_delete(message):
    with open('secrets.txt', 'a') as f:
        f.write(message.content + ' - ' + message.author.name + '\n') 
    reply = random.choice(deleteArr)
    await client.send_message(message.channel, reply)

@client.event
async def on_member_join(member):
    reply = 'Hej hej ' + member.name + '! :)'
    await client.send_message(member.server.get_channel('246343097611583488'), reply)

with open('keys/discordkey.txt', 'r') as f:
    key = f.readline()
client.run(key)