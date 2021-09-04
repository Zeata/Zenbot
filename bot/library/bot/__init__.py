from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
import os

PREFIX = "!zb"
OWNER_IDS = [163890141834772480]

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        super().__init__(command_prefix = PREFIX, owner_ids = OWNER_IDS)

    def run(self, version):
        self.VERSION = version 

        self.TOKEN = os.environ.get("DISCORDTOKEN")

        print("Running Bot...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print('Logged on as')
        print('{0.user}'.format(self))
        print(self.user.id)
        print('---------')

    async def on_disconnect(self):
        print("Bot_Disconnected")

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            print("Bot Ready")

        else:
            print("Bot Reconnect")

    async def on_message(self, message):
        pass

bot = Bot()