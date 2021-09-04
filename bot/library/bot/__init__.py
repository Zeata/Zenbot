from datetime import date, datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import channel
from discord import Embed
from discord.ext.commands import Bot as BotBase
import os

from discord.flags import Intents

PREFIX = "!zb"
OWNER_IDS = [163890141834772480]

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        super().__init__(
            command_prefix = PREFIX, 
            owner_ids = OWNER_IDS,
            intents = Intents.all(),
        )

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

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":

            await args[0].send("Someting went wrong")

        raise

    async def on_command_error(self, context, exception):
        return await super().on_command_error(context, exception)

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(330818023071940609)
            print("Bot Ready")

            channel = self.get_channel(883561872203337728)
            await channel.send("Now online!")

            embed = Embed(title = "Now Online!", description = "Zenbot is now online.", 
                          colour = 0xff0000, timestamp = datetime.utcnow())
            fields = [("Name", "Value", True),
                      ("Another Field", "The Next Field", True),
                      ("The Non Inline Field", "the vlas on its one", False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_author(name='{0.user}'.format(self), icon_url=self.guild.icon_url)
            embed.set_footer(text="This is a footer")
            await channel.send(embed=embed)

        else:
            print("Bot Reconnect")

    async def on_message(self, message):
        pass

bot = Bot()