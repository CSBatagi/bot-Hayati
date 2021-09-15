import asyncio
from asyncio.tasks import sleep
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

    async def on_timer_tick(self, phase, done, remaining):
        print(f'Phase {phase} with {done} seconds done and {remaining} seconds remaining.')
        
        # Countdown is delivered as one audio file to avoid stuttering due to rate limiting, routing etc.
        if remaining == 10 * 60:
            # Note that this seems to be non-blocking without wrapping it into a task or alike.
            await self.play('sounds/Event001_10DakikaAra.mp3')

        if remaining == 5 * 60:
            # Note that this seems to be non-blocking without wrapping it into a task or alike.
            await self.play('sounds/Event002_5DakikaKaldi.mp3')

        if remaining == 3 * 60:
            await self.play('sounds/Event003_3DakikaKaldi.mp3')

        if remaining == 60:
            await self.play('sounds/Event004_1DakikaKaldi.mp3')

    def on_timer_started(self):
        self._voice_client.play(discord.FFmpegPCMAudio('sounds/timer-set.mp3'))

    def on_timer_ended(self):
        self.play('sounds/Event005_MacBasliyor.mp3')

    def detach(self):
        self._timer.started -= self.on_timer_started
        self._timer.tick -= self.on_timer_tick
        self._timer.ended -= self.on_timer_ended
    
    async def play(self, mp3):
        for i, id in enumerate(c.voice_channels):
            if i == 0:
                channel = self._client.get_channel(id)
                voice_client = await channel.connect()
            else:
                await voice_client.move_to(self._client.get_channel(id))

            voice_client.play(discord.FFmpegPCMAudio(mp3))
            while voice_client.is_playing():
                await sleep(1)

        await voice_client.disconnect()

            
    


