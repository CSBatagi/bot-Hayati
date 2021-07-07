import os 
import sys 
from itertools import compress, chain
import discord
from discord.ext import commands 
from dotenv import load_dotenv
import random

from gsheet import gsheet 
import constants as c

import logging

logging.basicConfig(stream=sys.stdout, encoding='utf-8', level=int(os.getenv('LOGLEVEL')), 
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

sheet = gsheet()
#client = commands.Bot(command_prefix=commands.when_mentioned) 
intents = discord.Intents.all()
client = discord.Client(intents=intents)

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
  
@client.event
async def on_ready():
    print('SA moruklar ben {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    if client.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
        pass
    else:
        return

    msg = message.content.lower() 
    if "kadro" in msg or ("gelen" in msg and ("say" in msg or "liste" in msg)):    

        await message.channel.send("Bi sn ekranlarimi kontrol ediyorum..")

        _, player_status_name = get_player_status("gelen")
        msg_bck ="\n" #+ "\n".join(["".join(a) for i, a  in enumerate(liste) if join_list[i]])
        toplam = 0

        for name, status in player_status_name.items():
            if status: 
                msg_bck += "".join(name) + "\n"
                toplam += 1

        msg_bck = f"Toplam {toplam} kisi geliyor:\n" + msg_bck
        await message.channel.send(msg_bck)
    
    elif "gelmeyen" in msg or "satan" in msg:    

        liste = sheet.get(c.SPREADSHEET_ID, c.PLAYER_RANGE ) 
        not_join_list = sheet.get(c.SPREADSHEET_ID, c.NOT_JOIN_RANGE) 
        not_join_list_app = sheet.get(c.SPREADSHEET_ID, c.NOT_JOIN_RANGE) 
        msg_bck ="\n" #+ "\n".join(["".join(a) for i, a  in enumerate(liste) if join_list[i]])
        toplam = 0

        for i, isim in enumerate(liste):
            if not_join_list[i] == ['TRUE'] or not_join_list_app[i] == ['TRUE'] :
                msg_bck += "".join(isim) + "\n"
                toplam += 1

        msg_bck = f"Bu gotler varya bu gotler.. Toplam {toplam} kisi bu gotler:\n" + msg_bck

        await message.channel.send(msg_bck)

    elif "ben" in msg and "ekle" in msg:
        
        await message.channel.send("Bi sn ekranlarimi kontrol ediyorum..")

        steam_id = c.PLAYER_DISCORD[message.author.id] 
        mapp = get_recent_name_map()
        name = mapp[steam_id].strip()
        liste = sheet.get(c.SPREADSHEET_ID, c.PLAYER_RANGE ) 
        join_list = sheet.get(c.SPREADSHEET_ID, c.JOIN_RANGE) 
        not_join_list = sheet.get(c.SPREADSHEET_ID, c.NOT_JOIN_RANGE)
        for i, isim in enumerate(liste):
            logging.debug(f"Steam Id:{steam_id}, Name from map: {name}, Match Candidate: {isim}")
            if "".join(isim).strip() == name:
                join_list[i] = ['TRUE']
                not_join_list[i] = ['FALSE']
                sheet.update(c.SPREADSHEET_ID, c.JOIN_RANGE, join_list)
                sheet.update(c.SPREADSHEET_ID, c.NOT_JOIN_RANGE, not_join_list)
                await message.channel.send(f"Senin rumuz **{name}** di mi? Ekledim.")
                return 

        await message.channel.send("Listede yoksun ki lan!?") 
        
    elif "ekle" in msg or "geliyo" in msg or "gelice" in msg:

        await message.channel.send("Bi sn ekranlarimi kontrol ediyorum..")

        liste = sheet.get(c.SPREADSHEET_ID, c.PLAYER_RANGE ) 
        join_list = sheet.get(c.SPREADSHEET_ID, c.JOIN_RANGE) 
        not_join_list = sheet.get(c.SPREADSHEET_ID, c.NOT_JOIN_RANGE)
        
        for i, isim in enumerate(liste):
            if "".join(isim).lower() in msg:
                join_list[i] = ['TRUE']
                not_join_list[i] = ['FALSE']
                sheet.update(c.SPREADSHEET_ID, c.JOIN_RANGE, join_list)
                sheet.update(c.SPREADSHEET_ID, c.NOT_JOIN_RANGE, not_join_list)
                await message.channel.send("Bu bebeyi ekledim: " + "".join(isim))
                return 

        await message.channel.send("Böyle biri listede yok ki a.q napam ben simdi?") 

    elif "cikar" in msg or "çıkar" in msg or "gelmiyo" in msg or "gelmice" in msg:

        await message.channel.send("Bi sn ekranlarimi kontrol ediyorum..")

        liste = sheet.get(c.SPREADSHEET_ID, c.PLAYER_RANGE ) 
        join_list = sheet.get(c.SPREADSHEET_ID, c.JOIN_RANGE) 
        not_join_list = sheet.get(c.SPREADSHEET_ID, c.NOT_JOIN_RANGE) 
        
        for i, isim in enumerate(liste):
            if "".join(isim).lower() in msg:
                join_list[i] = ['FALSE']
                not_join_list[i] = ['TRUE']
                sheet.update(c.SPREADSHEET_ID, c.JOIN_RANGE, join_list)
                sheet.update(c.SPREADSHEET_ID, c.NOT_JOIN_RANGE, not_join_list)
                await message.channel.send("Bu iti listeden cikardim, siktirsin gitsin aq cocugu: " + "".join(isim))
                return 

        await message.channel.send("Böyle biri listede yok ki a.q napam ben simdi?") 

    elif "darla" in msg:
        await message.channel.send("Bi sn ekranlarimi kontrol ediyorum..")

        steamid_map, _ = get_player_status()
        try:
            members = message.guild.members
        except:
            raise discord.DiscordException
        darla_msg = f""
        
        for member in members:
            if not member.id in c.PLAYER_DISCORD:
                continue
            steam_id = c.PLAYER_DISCORD[member.id] 
            if steam_id in steamid_map and (not steamid_map[steam_id]):
                darla_msg += f"{member.mention}\n"

        if darla_msg:
            await message.channel.send(darla_msg + random.choice(c.darla_cumleleri))
        else:
                await message.channel.send("Darlicak adam yok olm oha!")
            
    elif "@here" in msg:
        return
            
    else:
        await message.channel.send("Buyur abi?")

def get_recent_name_map():
    player_ids = sheet.get(c.SPREADSHEET_ID, c.PLAYER_IDS)
    steam_to_name_map = {}
    for row in player_ids:
        steam_to_name_map[row[0]] = row[1]
    return steam_to_name_map


def get_player_status(typ="darla"):
    player_ids = sheet.get(c.SPREADSHEET_ID, c.PLAYER_IDS)
    liste = list(chain(*sheet.get(c.SPREADSHEET_ID, c.PLAYER_RANGE)))
    
    join_list = list(chain(*sheet.get(c.SPREADSHEET_ID, c.JOIN_RANGE)))
    string_to_bool(join_list)
    not_join_list = list(chain(*sheet.get(c.SPREADSHEET_ID, c.NOT_JOIN_RANGE)))
    string_to_bool(not_join_list)
    join_list_app = list(chain(*sheet.get(c.SPREADSHEET_ID, c.JOIN_RANGE_APP)))
    string_to_bool(join_list_app)
    not_join_list_app = list(chain(*sheet.get(c.SPREADSHEET_ID, c.NOT_JOIN_RANGE_APP)))
    string_to_bool(not_join_list_app)
    liste = list(chain(*sheet.get(c.SPREADSHEET_ID, c.PLAYER_RANGE)))
    
    
    if typ == "darla":

        response_list =  [join_list[i] or not_join_list[i] or 
                        not_join_list_app[i] or join_list_app[i]
                        for i in range(len(join_list))]
    else:
        response_list =  [join_list[i] or join_list_app[i]
                            for i in range(len(join_list))]

    
    #nested looplari azaltalim
    player_status_steam = {}
    player_status_name = {}
    name_to_steam_map = {}

    for m in player_ids:
        name_to_steam_map[m[1]] = m[0]

    for i, name in enumerate(liste):
        if name in name_to_steam_map:
            steam_id = name_to_steam_map[name]
            player_status_steam[steam_id] = response_list[i]
            player_status_name[name] = response_list[i]

    return player_status_steam, player_status_name 
def string_to_bool(liste):
    for i, s in enumerate(liste):
        if s == 'FALSE':
            liste[i] = False
        elif s == 'TRUE':
            liste[i] = True


client.run(BOT_TOKEN) # Add bot token here
