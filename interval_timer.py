import asyncio
from asyncio.tasks import sleep
from datetime import datetime, timedelta
import pytz

from event import Event


class IntervalTimer:
    def __init__(self):
        # Set up the events that any announcement services can listen to.
        self.started = Event()
        self.tick = Event()
        self.ended = Event()
        self._lock = False
        self._task = None
        self._end = None
        self._tz = pytz.timezone('Europe/Istanbul')

    def lock(self):
        self._lock = True

    def unlock(self):
        self._lock = False

    def is_locked(self):
        return self._lock

    def is_running(self):
        return not (self._task is None or self._task.done())

    async def start(self, minutes: int = None, until: tuple = None):
        await self.started.invoke()
        start = datetime.now(tz=self._tz)
        if minutes:
            self._end = start + timedelta(minutes=minutes, seconds=1)
        elif until:
            self._end = start.replace(hour=until[0], minute=until[1], second=1)
        else:
            return 'sictim burda abiler'

        self._task = asyncio.create_task(self._run_timer())
        # await self.started.invoke()
        time_left = self._end - start
        return f"{round(time_left.total_seconds() / 60)} dakika geri saymaya basladim."

    async def stop(self, channel):
        if self._lock:
            await channel.send('Bi sn a.q anons yapiyoz')
        while self._lock:
            await sleep(1)
        self._task.cancel()
        await channel.send('Saymayi biraktim burda')

    async def _run_timer(self):
        while datetime.now(tz=self._tz) < self._end:
            await sleep(1)
            remaining = self._end - datetime.now(tz=self._tz)
            remaining = remaining if remaining > timedelta(0) else timedelta(0)
            await self.tick.invoke(remaining=remaining)

        # Wait to not clash with the last tick event.
        await self.ended.invoke()
        print('Last interval completed.')
