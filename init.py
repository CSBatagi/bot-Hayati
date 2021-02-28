import os 
from itertools import compress, chain
import discord
from discord.ext import commands 
from dotenv import load_dotenv
import random

from gsheet import gsheet 
import constants as c

sheet = gsheet()
#client = commands.Bot(command_prefix=commands.when_mentioned) 
intents = discord.Intents.all()
client = discord.Client(intents=intents)

load_dotenv()
SPREADSHEET_ID= os.getenv('SPREADSHEET_ID') # Add ID here
JOIN_RANGE = os.getenv('JOIN_RANGE')
NOT_JOIN_RANGE = os.getenv('NOT_JOIN_RANGE')
ALL_JOIN_RANGE = os.getenv('ALL_JOIN_RANGE')
PLAYER_RANGE = os.getenv('PLAYER_RANGE')
BOT_TOKEN = os.getenv('BOT_TOKEN')
PLAYER_IDS=os.getenv('PLAYER_IDS')
  
@client.event
async def on_ready():
    print('SA moruklar ben {0.user}'.format(client))

@client.event

async def on_message(message):
    if message.author == client.user:
        return
        
    if not client.user.mentioned_in(message):
        return

    try: 
    #await message.channel.send('Selam moruklar ben Hayati')
        msg = message.content.lower() 
        if "kadro" in msg or ("gelen" in msg and ("say" in msg or "liste" in msg)):    

            liste = sheet.get(SPREADSHEET_ID, ALL_JOIN_RANGE )         
            msg_bck ="\n" #+ "\n".join(["".join(a) for i, a  in enumerate(liste) if join_list[i]])
            toplam = 0

            for i, isim in enumerate(liste):
                if i == 0:
                    tarih = "".join(isim)
                    continue
                if isim:
                    msg_bck += "".join(isim) + "\n"
                    toplam += 1

            msg_bck = f"Mac tarihi: {tarih}, toplam {toplam} kisi geliyor:\n" + msg_bck
            await message.channel.send(msg_bck)
        
        elif "gelmeyen" in msg or "satan" in msg:    

            liste = sheet.get(SPREADSHEET_ID, PLAYER_RANGE ) 
            not_join_list = sheet.get(SPREADSHEET_ID, NOT_JOIN_RANGE) 
            msg_bck ="\n" #+ "\n".join(["".join(a) for i, a  in enumerate(liste) if join_list[i]])
            toplam = 0

            for i, isim in enumerate(liste):
                if not_join_list[i] == ['TRUE']:
                    msg_bck += "".join(isim) + "\n"
                    toplam += 1

            msg_bck = f"Bu gotler varya bu gotler.. Toplam {toplam} kisi bu gotler:\n" + msg_bck
            await message.channel.send(msg_bck)

        elif "ekle" in msg or "geliyo" in msg or "gelice" in msg:

            liste = sheet.get(SPREADSHEET_ID, PLAYER_RANGE ) 
            join_list = sheet.get(SPREADSHEET_ID, JOIN_RANGE) 
            not_join_list = sheet.get(SPREADSHEET_ID, NOT_JOIN_RANGE)
            
            for i, isim in enumerate(liste):
                if "".join(isim).lower() in msg:
                    join_list[i] = ['TRUE']
                    not_join_list[i] = ['FALSE']
                    sheet.update(SPREADSHEET_ID, JOIN_RANGE, join_list)
                    sheet.update(SPREADSHEET_ID, NOT_JOIN_RANGE, not_join_list)
                    await message.channel.send("Bu bebeyi ekledim: " + "".join(isim))
                    return 

            await message.channel.send("Böyle biri listede yok ki a.q napam ben simdi?") 

        elif "cikar" in msg or "çıkar" in msg or "gelmiyo" in msg or "gelmice" in msg:
            liste = sheet.get(SPREADSHEET_ID, PLAYER_RANGE ) 
            join_list = sheet.get(SPREADSHEET_ID, JOIN_RANGE) 
            not_join_list = sheet.get(SPREADSHEET_ID, NOT_JOIN_RANGE) 
            

            for i, isim in enumerate(liste):
                if "".join(isim).lower() in msg:
                    join_list[i] = ['FALSE']
                    not_join_list[i] = ['TRUE']
                    sheet.update(SPREADSHEET_ID, JOIN_RANGE, join_list)
                    sheet.update(SPREADSHEET_ID, NOT_JOIN_RANGE, not_join_list)
                    await message.channel.send("Bu iti listeden cikardim, siktirsin gitsin aq cocugu: " + "".join(isim))
                    return 

            await message.channel.send("Böyle biri listede yok ki a.q napam ben simdi?") 

        elif "darla" in msg:

            liste = sheet.get(SPREADSHEET_ID, PLAYER_IDS)
            
            members = message.guild.members


            join_list = list(chain(*sheet.get(SPREADSHEET_ID, JOIN_RANGE)))
            not_join_list = list(chain(*sheet.get(SPREADSHEET_ID, NOT_JOIN_RANGE)))
            # TODO: Umut appten geliyorum diyenler icin kolon acinda buraya appten geliyorum diyenleri de or ile eklemek gerek
            response_list =  [join_list[i] or not_join_list[i] for i in range(len(join_list))]
            player_ids = sheet.get(SPREADSHEET_ID, PLAYER_RANGE)

            for idx, player_id in enumerate(player_ids):
                player_id = player_id[0]
                if response_list[idx] == 'FALSE':
                    for steam_map in liste:
                        if player_id in steam_map:
                            for member in members:
                                try:
                                    print(member.name, c.PLAYER_DISCORD[steam_map[0]])
                                    if member.name == c.PLAYER_DISCORD[steam_map[0]]:
                                        darla_msg = random.choice(c.darla_cumleleri)
                                        await message.channel.send(f"{member.mention} {darla_msg}")
                                except:
                                    continue

        elif "@here" in msg:
            return
               
        else:
            await message.channel.send("Buyur abi?")

    except:
        raise discord.DiscordException
            
client.run(BOT_TOKEN) # Add bot token here
