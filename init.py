import os 
import discord
#from discord.ext import commands 
from dotenv import load_dotenv

from gsheet import gsheet 

sheet = gsheet()
#client = commands.Bot(command_prefix=commands.when_mentioned) 
client = discord.Client()

load_dotenv()
SPREADSHEET_ID= os.getenv('SPREADSHEET_ID') # Add ID here
JOIN_RANGE = os.getenv('JOIN_RANGE')
NOT_JOIN_RANGE = os.getenv('NOT_JOIN_RANGE')
PLAYER_RANGE = os.getenv('PLAYER_RANGE')
BOT_TOKEN = os.getenv('BOT_TOKEN')
  
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

            liste = sheet.get(SPREADSHEET_ID, PLAYER_RANGE ) 
            join_list = sheet.get(SPREADSHEET_ID, JOIN_RANGE) 
            msg_bck ="\n" #+ "\n".join(["".join(a) for i, a  in enumerate(liste) if join_list[i]])
            toplam = 0

            for i, isim in enumerate(liste):
                if join_list[i] == ['TRUE']:
                    msg_bck += "".join(isim) + "\n"
                    toplam += 1

            msg_bck = f"Al A.Q toplam {toplam} kisi geliyor:\n" + msg_bck
            await message.channel.send(msg_bck)
        
        if "gelmeyen" in msg or "satan" in msg:    

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

        else:
            await message.channel.send("Buyur abi?")

    except:
        raise discord.DiscordException
            
client.run(BOT_TOKEN) # Add bot token here
