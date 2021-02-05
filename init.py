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
        if "gelen" in msg and ("say" in msg or "liste" in msg):    
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
        elif "ekle" in msg or "geliyorum" in msg or "gelicem" in msg:
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

        elif "cikar" in msg or "çıkar" in msg or "gelmiyor" in msg or "gelmice" in msg:
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
            await message.channel.send("".join(isim) + " listede yok ki a.q napam ben simdi?") 

        else:
            await message.channel.send("Buyur abi?")
    except:
        raise discord.DiscordException

            
    # # Restrict the command to a role
    # # Change REQUIREDROLE to a role id or None
    # REQUIREDROLE = None
    # if REQUIREDROLE is not None and discord.utils.get(message.author.roles, id=str(REQUIREDROLE)) is None:
    #     await message.channel.send('You don\'t have the required role!')
    #     return

    # # Command to insert data to excel
    # if message.content.startswith('!s '):

    #     msg = message.content[3:]
    #     result = [x.strip() for x in msg.split(',')]
    #     if len(result) == FIELDS:
    #         # Add
    #         print(message.created_at)
    #         DATA = [message.author.name] + [str(message.author.id)] + [str(message.created_at)] + result
    #         sheet.add(SPREADSHEET_ID, RANGE_NAME, DATA)
    #         await message.channel.send('Your data has been successfully submitted!')
    #     else:
    #         # Needs more/less fields
    #         await message.channel.send('Error: You need to add {0} fields, meaning it can only have {1} comma.'.format(FIELDS,FIELDS-1))
    
    # # Whois
    # # Please dont remove the copyright and github repo
    # elif len(message.mentions) > 0:
    #     for muser in message.mentions:
    #         if muser.id == client.user.id:
    #             if any(word in message.content for word in ['whois','who is','Help','help','info']):
    #                 await message.channel.send('This bot was made by hugonun(https://github.com/hugonun/).\nSource code: https://github.com/hugonun/discord2sheet-bot')


client.run(BOT_TOKEN) # Add bot token here
