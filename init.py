from gsheet import GSheet
import os 
from itertools import chain
import discord
from discord.ext import commands 
from dotenv import load_dotenv
import random


from interval_timer import IntervalTimer
from voice_announcer import VoiceAnnouncer

import logging.config
import constants as c

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

#client = commands.Bot(command_prefix=commands.when_mentioned) 
intents = discord.Intents.all()
client = discord.Client(intents=intents)
sheet = GSheet()

load_dotenv()
##voice 
bot = commands.Bot(command_prefix='!')
timer = IntervalTimer()
voice_announcer = None
  
@client.event
async def on_ready():
    print('SA moruklar ben {0.user}'.format(client))

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
        
    if client.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
        pass
    else:
        return

    msg = message.content.lower().strip().split() 
    if '@' in msg[0]:
        msg.pop(0)
    msg ="".join(msg)

    if "kadro" in msg or ("gelen" in msg and ("say" in msg or "liste" in msg)):    

        await message.channel.send("Bi sn ekranlarimi kontrol ediyorum..")

        _, player_status_name = await sheet.get_player_status("gelen")
        msg_bck ="\n" #+ "\n".join(["".join(a) for i, a  in enumerate(liste) if join_list[i]])
        toplam = 0

        for name, status in player_status_name.items():
            if status: 
                msg_bck += "".join(name) + "\n"
                toplam += 1

        msg_bck = f"Toplam {toplam} kisi geliyor:\n" + msg_bck
        await message.channel.send(msg_bck)
    
    elif "gelmeyen" in msg or "satan" in msg:    
        await message.channel.send("Bi sn ekranlarimi kontrol ediyorum..")

        msg_bck, toplam = await sheet.not_coming()
        msg_bck = f"Bu gotler varya bu gotler.. Toplam **{toplam}** kisi bu gotler:\n" + msg_bck

        await message.channel.send(msg_bck)

    elif ("ben" in msg and "ekle" in msg) or ("ekle" == msg):

        await message.channel.send("Bi sn ekranlarimi kontrol ediyorum..")
        steam_id = c.PLAYER_DISCORD[message.author.id] 
        name = await sheet.add(steam_id = steam_id)
        if name: 
            await message.channel.send(f"Senin rumuz **{name}** di mi? Ekledim.")
        else:
            await message.channel.send("Listede yoksun ki lan!?") 
        
    elif "ekle" in msg or "geliyo" in msg or "gelice" in msg:

        await message.channel.send("Bi sn ekranlarimi kontrol ediyorum..")
        name = await sheet.add(msg = msg)
        if name: 
            await message.channel.send(f"Senin rumuz **{name}** di mi? Ekledim.")
        else:
            await message.channel.send("Böyle biri listede yok ki a.q napam ben simdi?") 

    elif ("ben" in msg and (("cikar" in msg) or ("çıkar" in msg)) or (("çıkar" == msg) or ("cikar" == msg))):

        await message.channel.send("Bi sn ekranlarimi kontrol ediyorum..")
        steam_id = c.PLAYER_DISCORD[message.author.id] 
        name = await sheet.remove(steam_id = steam_id)
        if name: 
            await message.channel.send("Bu iti listeden cikardim, siktirsin gitsin aq cocugu: **"
                                        + "**".join(name) + "**")
        else:
            await message.channel.send("Listede yoksun ki lan!?")            

    elif "cikar" in msg or "çıkar" in msg or "gelmiyo" in msg or "gelmice" in msg:

        await message.channel.send("Bi sn ekranlarimi kontrol ediyorum..")
        name = await sheet.remove(msg=msg)
        if name:
            await message.channel.send("Bu iti listeden cikardim, siktirsin gitsin aq cocugu: **" 
                                        + "**".join(name) + "**")
        else:
            await message.channel.send("Böyle biri listede yok ki a.q napam ben simdi?") 

    elif "darla" in msg:
        await message.channel.send("Bi sn ekranlarimi kontrol ediyorum..")
        try:
            members = message.guild.members
        except:
            raise discord.DiscordException

        darla_msg = await sheet.darla(members)

        if darla_msg:
            await message.channel.send(darla_msg + random.choice(c.darla_cumleleri))
        else:
                await message.channel.send("Darlicak adam yok olm oha!")
            
    elif "@here" in msg:
        return
            
    else:
        await message.channel.send("Buyur abi?")


client.run(os.getenv('BOT_TOKEN')) # Add bot token here
