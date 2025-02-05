import logging
import logging.config
import os
import random
import re
import asyncio

import discord
from dotenv import load_dotenv

import constants as c
from gcp import GcpCompute
from gpt import Gpt
from gsheet import GSheet
from interval_timer import IntervalTimer
from voice_announcer import VoiceAnnouncer

logging.config.fileConfig("logging.conf")
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

intents = discord.Intents.default()
intents.members = True
# client = commands.Bot(command_prefix='!', intents=intents)
client = discord.Client(intents=intents)
sheet = GSheet()
gcp_16 = GcpCompute(c.server_cs16['zone'], c.server_cs16['instance'], c.server_cs16['subdomain'])
gcp_2 = GcpCompute(c.server_cs2['zone'], c.server_cs2['instance'], c.server_cs2['subdomain'])
get5 = GcpCompute(c.get5['zone'], c.get5['instance'], c.get5['subdomain'])

gptObj = Gpt()

load_dotenv()

timer = IntervalTimer()
voice_announcer = VoiceAnnouncer(client, timer)


async def gpt(ctx):
    logging.info('Sending to gpt')
    raw_text = gptObj.generate_text(ctx.message.content)
    text = gptObj.clean_text(raw_text)
    await ctx.send(text)


@client.event
async def on_ready():
    logging.info('SA moruklar ben {0.user}'.format(client))


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if message.mention_everyone:
        return

    if client.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
        pass
    else:
        return

    msg = message.content.strip().split()
    if '@' in msg[0]:
        msg.pop(0)
    msg = "".join(msg)

    if message.channel.id == c.genel_channel_id:
        logging.info('Sending to gpt')
        raw_text = gptObj.generate_text(msg)
        text = gptObj.clean_text(raw_text)
        await message.channel.send(text)
        return

    msg = msg.lower()

    if "kadro" in msg or ("gelen" in msg and ("say" in msg or "liste" in msg)):

        await message.channel.send("Bi sn ekranlarimi kontrol ediyorum..")

        msg_bck = await kadro_yaz()
        await message.channel.send(msg_bck)

    elif "gelmeyen" in msg or "satan" in msg:
        await message.channel.send("Bi sn ekranlarimi kontrol ediyorum..")

        msg_bck, toplam = await sheet.not_coming()
        msg_bck = f"Bu gotler varya bu gotler.. Toplam **{toplam}** kisi bu gotler:\n" + msg_bck

        await message.channel.send(msg_bck)

    elif "ekle" in msg or "geliyo" in msg or "gelice" in msg:

        await message.channel.send("Bi sn ekranlarimi kontrol ediyorum..")
        steam_id = c.PLAYER_DISCORD[message.author.id]
        if name := await sheet.add(msg=msg):
            await message.channel.send(f"Bu aslan bu aslan. **{name}** eklendi.")
            await message.channel.send(await kadro_yaz())
        elif name := await sheet.add(steam_id=steam_id):
            await message.channel.send(f"Senin rumuz **{name}** di mi? Ekledim.")
            await message.channel.send(await kadro_yaz())
        else:
            await message.channel.send("Böyle biri listede yok ki a.q napam ben simdi?")

    elif "ben" in msg and (("cikar" in msg) or ("çıkar" in msg)) or (("çıkar" == msg) or ("cikar" == msg)):

        await message.channel.send("Bi sn ekranlarimi kontrol ediyorum..")
        steam_id = c.PLAYER_DISCORD[message.author.id]
        name = await sheet.remove(steam_id=steam_id)
        if name:
            await message.channel.send(f"Bu iti listeden cikardim, siktirsin gitsin aq cocugu: **{name}**")
            await message.channel.send(await kadro_yaz())
        else:
            await message.channel.send("Listede yoksun ki lan!?")

    elif "cikar" in msg or "çıkar" in msg or "gelmiyo" in msg or "gelmice" in msg:

        await message.channel.send("Bi sn ekranlarimi kontrol ediyorum..")
        name = await sheet.remove(msg=msg)
        if name:
            await message.channel.send(f"Bu iti listeden cikardim, siktirsin gitsin aq cocugu: **{name}**")
            await message.channel.send(await kadro_yaz())
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
    elif "say" in message.content.lower().split():

        if timer.is_running():
            await message.channel.send('Hala sayiyorum ulan kac tane isi yapicam?')
            return
        msglist = message.content.lower().split()
        for m in msglist:
            if re.match('^[0-9]+$', m):
                time_left = await timer.start(minutes=int(m))
                msg = await message.channel.send(time_left)
                voice_announcer.set_message(msg)
                return
            elif re.match('^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', m):
                digits = m.split(":")
                digits = int(digits[0]), int(digits[1])
                time_left = await timer.start(until=digits)
                msg = await message.channel.send(time_left)
                voice_announcer.set_message(msg)

                return
        await message.channel.send("Neye sayayim a.q")

    elif "dur" == msg:
        await timer.stop(message.channel)

    # elif "server" in msg and ("16" in msg or "1.6" in msg):
    #         await gcp_16.start_instance(message.channel)
    elif "server" in msg and ("ac" in msg or "aç" in msg):
            await asyncio.gather(gcp_2.start_instance(message.channel), get5.start_instance(message.channel))

    elif "server" in msg and "kapa" in msg:
        await message.channel.send(" Kapatma komutunu verdim..")
        # await asyncio.gather(gcp_16.stop_instance(message.channel), gcp_2.stop_instance(message.channel), get5.stop_instance(message.channel))
        await asyncio.gather(gcp_2.stop_instance(message.channel), get5.stop_instance(message.channel))

    else:
        await message.channel.send(c.buyur_abi)


async def kadro_yaz():
    _, player_status_name = await sheet.get_player_status("gelen")
    msg_bck = "\n"  # + "\n".join(["".join(a) for i, a  in enumerate(liste) if join_list[i]])
    toplam = 0

    for name, status in player_status_name.items():
        if status:
            msg_bck += "".join(name) + "\n"
            toplam += 1

    return f"Toplam {toplam} kisi geliyor:\n" + msg_bck


client.run(os.getenv('BOT_TOKEN'))  # Add bot token here
