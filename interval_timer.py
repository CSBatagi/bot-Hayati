import asyncio
import enum
import datetime

from event import Event

class IntervalTimer:
    def __init__(self):
        # Set up the events that any announcement services can listen to.
        self.started = Event()
        self.tick = Event()
        self.ended = Event()

        self._seconds = 10 * 60

        self._task = None

    def running(self):
        return not (self._task is None or self._task.done())

    def print_config(self):
        return f'{round(self._seconds / 60)} dakika geri saymaya basladim'

    async def start(self, minutes: int = None, until: tuple = None):
        if minutes:
            self._seconds = minutes * 60 + 2
        elif until:
            timenow = datetime.datetime.now()
            deadline = timenow.replace(hour = until[0], minute = until[1]) 
            timeleft = deadline - timenow 
            self._seconds = timeleft.seconds + 2
        else:
            return 'sictim burda abiler'
        
        self._task = asyncio.create_task(self._run_timer())
        await self.started.invoke()
        return f'Saymaya basladim {self._seconds / 60} dakika kaldi.'

    def stop(self):
        self._task.cancel()
        return 'Saymayi biraktim burda'

    async def _run_timer(self):
        
        seconds_passed = 0
        while seconds_passed < self._seconds:
            await asyncio.sleep(1)
            seconds_passed += 1
            await self.tick.invoke(phase=1, done=seconds_passed, remaining=self._seconds - seconds_passed)
        
        # Wait to not clash with the last tick event.
        await asyncio.sleep(1)
        await self.ended.invoke()
        print('Last interval completed.')