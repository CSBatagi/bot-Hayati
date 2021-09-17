import datetime
from asyncio.tasks import create_task,sleep 
import discord

from interval_timer import IntervalTimer 

import constants as c 

class VoiceAnnouncer():
    def __init__(self, client: discord.Client, timer:IntervalTimer):
        self._client = client
        self._timer = timer 
        ##timer.started += self.on_timer_started
        timer.tick += self.on_timer_tick
        timer.ended += self.on_timer_ended
        self.message = None
        self.message_content = None
    def set_message(self, msg):
        self.message_content = msg.content
        self.message = msg

    async def on_timer_tick(self, phase, done, remaining):
        new_content = f" Kalan zaman: {datetime.timedelta(seconds=remaining)}"
        await(self.message.edit(content = self.message_content + new_content)) 
        self._timer.lock()
        if remaining == 10 * 60+ 10:
            await self.play('sounds/Event001_10DakikaAra.mp3')

        if remaining == 5 * 60 + 10:
            await self.play('sounds/Event002_5DakikaKaldi.mp3')

        if remaining == 3 * 60 + 10:
            await self.play('sounds/Event003_3DakikaKaldi.mp3')

        if remaining == 60 + 10:
            await self.play('sounds/Event004_1DakikaKaldi.mp3')
        self._timer.unlock()

    async def on_timer_started(self):

        await self._voice_client.play(discord.FFmpegPCMAudio('sounds/timer-set.mp3'))

    async def on_timer_ended(self):
        self._timer.lock()
        await self.play('sounds/Event005_MacBasliyor.mp3')
        self.message = None
        self._timer.unlock()

    def detach(self):
        self._timer.started -= self.on_timer_started
        self._timer.tick -= self.on_timer_tick
        self._timer.ended -= self.on_timer_ended
        self.message = None
    
    async def play(self, mp3):
        for i, id in enumerate(c.voice_channels):
            if i == 0:
                channel = self._client.get_channel(id)
                voice_client = await channel.connect()
            else:
                await voice_client.move_to(self._client.get_channel(id))
            try:
                voice_client.play(discord.FFmpegPCMAudio(mp3))
                while voice_client.is_playing():
                    await sleep(1)
            except Exception as e:
                print(str(e)) 
                await sleep(1)
                await voice_client.disconnect()
                return
               
        await sleep(1)
        await voice_client.disconnect()
            
    


