from asyncio.tasks import create_task,sleep 
import discord

from interval_timer import IntervalTimer 

import constants as c 

class VoiceAnnouncer():
    def __init__(self, client: discord.Client, timer:IntervalTimer):
        self._client = client
        self._timer = timer 
        timer.started += self.on_timer_started
        timer.tick += self.message_updater
        timer.tick += self.on_timer_tick
        timer.ended += self.on_timer_ended
        self.reset_state()

    def reset_state(self):
        self._minute_marks = [10,5,3,1]
        self._sound_files = [
            'sounds/Event001_10DakikaAra.mp3',
            'sounds/Event002_5DakikaKaldi.mp3',
            'sounds/Event003_3DakikaKaldi.mp3',
            'sounds/Event004_1DakikaKaldi.mp3',
        ]
        self.message = None
        self.message_content = None

    def set_message(self, msg):
        self.message_content = msg.content
        self.message = msg

    async def message_updater(self, remaining):
        new_content = f" Kalan zaman: {str(remaining).split('.')[0]}"
        await(self.message.edit(content = self.message_content + new_content)) 

    async def on_timer_tick(self, remaining):
        remaining_minutes = round(remaining.total_seconds() / 60) 
        for i, mark in enumerate(self._minute_marks):
            if remaining_minutes == mark:
                create_task(self.play(self._sound_files[i]))
                self._minute_marks.pop(i)
                self._sound_files.pop(i)
        
    def on_timer_started(self):
        self.reset_state()

    async def on_timer_ended(self):
        create_task(self.play('sounds/Event005_MacBasliyor.mp3'))


    def detach(self):
        self._timer.started -= self.on_timer_started
        self._timer.tick -= self.on_timer_tick
        self._timer.ended -= self.on_timer_ended
        self.reset_state()
    
    async def play(self, mp3):

        while self._timer.is_locked():
            await sleep(1)
        self._timer.lock()
        try:
            for i, id in enumerate(c.voice_channels):
                channel = self._client.get_channel(id)
                if i == 0:
                    voice_client = await channel.connect()
                else:
                    await voice_client.move_to(channel)

                voice_client.play(discord.FFmpegPCMAudio(mp3))
                while voice_client.is_playing():
                    await sleep(1)

        except Exception as e:
            print(str(e)) 
        finally:
            self._timer.unlock()
            await sleep(1)
            await voice_client.disconnect()
            
            
    


