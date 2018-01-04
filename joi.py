import discord
import asyncio
import random
import time
import operator
import threading
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
foodArr = ['\U0001F35E', '\U0001F356', '\U0001F9C0', '\U0001F357', '\U0001F969', '\U0001F953', '\U0001F354', '\U0001F355', '\U0001F96A', '\U0001F32E', '\U0001F32F', '\U0001F959', '\U0001F373', '\U0001F958', '\U0001F372', '\U0001F963', '\U0001F957', '\U0001F371', '\U0001F961', '\U0001F375'];

soundDict = {
    'drum' : 'joke_drum_effect.mp3',
    'isis' : 'Saleel_Sawarim.mp3',
    'sad' : 'sadtrombone.mp3',
    'haha' : 'haha.mp3',
    'dun' : 'DUN_DUN.mp3',
    'clues' : 'clues.mp3',
    'clue' : 'clues.mp3'
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
    tmp = await client.send_message(message.channel, 'Räknar meddelanden...')
    counter = 0
    async for log in client.logs_from(message.channel, limit=100):
        if log.author == message.author:
            counter += 1
    await client.edit_message(tmp, 'Du har skrivit {} meddelanden senaste sessionen.'.format(counter))

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
    if localVoiceClient is None:
        if callUser.voice.voice_channel is None:
            await client.send_message(message.channel, 'Och var exakt hade du tänkt dig att det skulle ske?')
            return
        else:
            localVoiceClient = await client.join_voice_channel(callUser.voice.voice_channel)
    elif hasattr(message.author, 'voice'):
        if localVoiceClient.channel != message.author.voice.voice_channel:
            await localVoiceClient.disconnect()
            localVoiceClient = await client.join_voice_channel(callUser.voice.voice_channel)  
    player = localVoiceClient.create_ffmpeg_player(sound)
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
    await client.send_message(message.channel, 'Jag kan göra massa roliga saker! Bara skriv mitt namn och ett kommatecken följt av något av detta:\n* test - räkna meddelanden i en session. \n* var är @<user> - kollar var folk är. \n* kom; här - Om du vill ha in mig i din röstkanal. \n* sov; stick; dra - Om du vill att jag ska lämna din röstkanal. \n* play <drum, isis, haha, dun, clues, sad> - Om du vill ha en punchline ;) \n* roll, rulla <dice> - Om du vill att jag ska rulla lite tärningar. Ex: roll 3d6 4d10. \n* wiki me, reddit me - Om du vill ha en länk till en wikipediasida eller en subreddit. Ex: reddit me sweden. \n* news - Om du vill se seanste nytt. \n* r6 <stat> - Om du vill se stats för Rainbow6, t.ex kills, deaths, kd eller mystats. \n* teams - Dela in alla spelare i den nuvarande röstkanalen i två olika lag.')

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

async def joi_scrape_r6(message, client):
    
    statDict = {
    'kills' : 'Kills',
    'deaths' : 'Deaths',
    'kd' : 'K/D',
    'k/d' : 'K/D',
    'playtime' : 'Playtime',
    'record' : 'Record',
    'win' : 'Win %',
    '%' : 'Win %',
    'mystats' : 'myStats',
    'mystats' : 'myStats'
    }

    stats = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    stat_list = ['Kills', 'Deaths', 'K/D', 'Playtime', 'Record', 'Win %']
    reply = ''

    with open('players.txt') as f:
        player_list = f.readlines()
    player_list = [x.strip() for x in player_list] 

    stat_type = statDict.get(message.content.split(' ')[1])  
    if stat_type != 'myStats' and stat_type != None:
        for player in player_list:
            quote_page = 'https://r6stats.com/stats/uplay/' + player + '/ranked'
            req = urlRequest.Request(quote_page, headers = headers)
            url = urlRequest.urlopen(req)
            sourceCode = url.read()
            soup = BeautifulSoup(sourceCode, 'html.parser')
            stat_value = soup.find('div', text=stat_type).find_next_siblings('div')
            stats.append((player, int(stat_value[0].get_text().replace('\n', ''))))

        stats.sort(key=operator.itemgetter(1), reverse = True)

        reply = 'Jag hörde att du ville ha lite statistik' + '[' + stat_type + '] :\n'     
        for item in stats:
            reply = reply + item[0] + ': ' + str(item[1]) + '\n'

    elif stat_type == 'myStats':
        player = ubiDict.get(message.author.id)
        for stat in stat_list:
            quote_page = 'https://r6stats.com/stats/uplay/' + player + '/ranked'
            req = urlRequest.Request(quote_page, headers = headers)
            url = urlRequest.urlopen(req)
            sourceCode = url.read()
            soup = BeautifulSoup(sourceCode, 'html.parser')
            stat_value = soup.find('div', text=stat).find_next_siblings('div')
            stats.append(stat_value[0].get_text().replace('\n', ''))
        fav_op = soup.find('h3', attrs={'class': 'operator-name'})
        fav_op = fav_op.text.strip().capitalize()
        reply = 'Här är dina stats i Rainbow6:\n'
        i = 0
        for item in stats:
            reply = reply + '**' + stat_list[i] + ': **' + item + '\n'
            i = i + 1
        reply = reply + '**Favourite operator: **' + fav_op    
    else:
        reply = 'Jag tror inte jag hänger med. Du kan prova med t.ex kills, deaths eller mystats.'

    await client.send_message(message.channel, reply)

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

async def joi_teams(message, client):
    current_vc = discord.utils.find(lambda m: m.id == message.author.id, server.members).voice.voice_channel
    new_team_vc = None
    number_of_players = len(current_vc.voice_members)
    new_team_text = []
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
        team1 = mem.name + '\n'
    for mem in  new_team_text:
        team2 = mem.name + '\n'
    #await client.send_message(message.channel, random.choice(teamArr))
    reply = '**Lag 1: **\n' + team1 + '**Lag 2: **\n' + team2
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
    'r6' : joi_scrape_r6,
    'lag' : joi_teams,
    'teams' : joi_teams,
    'joke' : joi_scrape_joke
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

    if message.content.find('game') > -1:
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

    elif message.content.find('joi') > -1 and message.author.id != '386139218885476352':
        reply = random.choice(joiArr)
        await client.send_message(message.channel, reply)
    lock = False

@client.event
async def on_message_delete(message):
    reply = random.choice(deleteArr)
    await client.send_message(message.channel, reply)

@client.event
async def on_member_join(member):
    reply = 'Hej hej ' + member.name + '! :)'
    await client.send_message(member.server.get_channel('246343097611583488'), reply)

with open('key.txt', 'r') as f:
    key = f.readline()
client.run(key)