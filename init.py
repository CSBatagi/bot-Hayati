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
JOIN_RANGE_APP = os.getenv('JOIN_RANGE_APP')
NOT_JOIN_RANGE_APP = os.getenv('NOT_JOIN_RANGE_APP')
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
            await message.channel.send("Bi sn ekranlarimi kontrol ediyorum..")
            player_ids = sheet.get(SPREADSHEET_ID, PLAYER_IDS)
            join_list = list(chain(*sheet.get(SPREADSHEET_ID, JOIN_RANGE)))
            not_join_list = list(chain(*sheet.get(SPREADSHEET_ID, NOT_JOIN_RANGE)))
            join_list_app = list(chain(*sheet.get(SPREADSHEET_ID, JOIN_RANGE_APP)))
            not_join_list_app = list(chain(*sheet.get(SPREADSHEET_ID, NOT_JOIN_RANGE_APP)))
            # TODO: Umut appten geliyorum diyenler icin kolon acinda buraya appten geliyorum diyenleri de or ile eklemek gerek
            response_list =  [join_list[i] or not_join_list[i] or 
                              not_join_list_app[i] or join_list_app[i]
                              for i in range(len(join_list))]
        
            liste = sheet.get(SPREADSHEET_ID, PLAYER_RANGE)
            
            members = message.guild.members
            darla_msg = f""
            
            #nested looplari azaltalim
            steamid_map = {}
            recent_name_map = {}
            for m in player_ids:
                #steamid_map[m[0]] = m[1]
                recent_name_map[m[1]] = m[0]
            for i, name in enumerate(liste):
                if name[0] in recent_name_map:
                    steam_id = recent_name_map[name[0]]
                    steamid_map[steam_id] = response_list[i]
                
            for member in members:
                if not member.id in c.PLAYER_DISCORD:
                    continue
                steam_id = c.PLAYER_DISCORD[member.id] 
                if steam_id in steamid_map and steamid_map[steam_id] == 'FALSE':
                    darla_msg += f"{member.mention}\n"

            if darla_msg:
                await message.channel.send(darla_msg + random.choice(c.darla_cumleleri))
            else:
                await message.channel.send("Darlicak adam yok olm oha!")
            
        elif "@here" in msg:
            return
               
        else:
            await message.channel.send("Buyur abi?")

    except:
        raise discord.DiscordException
            
client.run(BOT_TOKEN) # Add bot token here
