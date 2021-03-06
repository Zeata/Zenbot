
from asyncio.tasks import sleep
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Embed
from discord.ext.commands import Bot as BotBase
from discord.ext.commands.core import Command
from discord.ext.commands.errors import CommandNotFound
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument,
								  CommandOnCooldown)
from discord.ext.commands import when_mentioned_or
from discord.errors import HTTPException, Forbidden
from discord.flags import Intents

from ..db import db
from glob import glob

from datetime import datetime
import os

PREFIX = "!zb"
OWNER_IDS = [163890141834772480]
COGS = [path.split("\\")[-1][:-3] for path in glob("./bot/library/cogs/*.py")]

def get_prefix(bot, message):
    return when_mentioned_or(PREFIX)(bot, message)

class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)
    
    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        super().__init__(
            command_prefix = get_prefix, 
            owner_ids = OWNER_IDS,
            intents = Intents.all(),
        )

    def setup(self):
        for cog in COGS:
            self.load_extension(f"bot.library.cogs.{cog}")
            print(f"{cog} cog loaded")

        print("Setup Complete")

    def run(self, version):
        self.VERSION = version 

        print ("Running Setup...")
        self.setup()

        self.TOKEN = os.environ.get("DISCORDTOKEN")

        print("Running Bot...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print('---------')
        print('Logged on as')
        print('{0.user}'.format(self))
        print(self.user.id)
        print('---------')

    async def on_disconnect(self):
        print("Bot_Disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Someting went wrong")


        await self.stdout.send("Now online!")

        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("One or more required arguments are missing.")

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f"That command is on {str(exc.cooldown.type).split('.')[-1]} cooldown. Try again in {exc.retry_after:,.2f} secs.")

        elif hasattr(exc, "original"):
            # if isinstance(exc.original, HTTPException):
            # 	await ctx.send("Unable to send message.")

            if isinstance(exc.original, Forbidden):
                await ctx.send("I do not have permission to do that.")

            else:
                raise exc.original

        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(330818023071940609)
            self.stdout = self.get_channel(883561872203337728)
            self.scheduler.start()
            await self.stdout.send("Now online!")

            # embed = Embed(title = "Now Online!", description = "Zenbot is now online.", 
            #               colour = 0xff0000, timestamp = datetime.utcnow())
            # fields = [("Name", "Value", True),
            #           ("Another Field", "The Next Field", True),
            #           ("The Non Inline Field", "the vlas on its one", False)]
            # for name, value, inline in fields:
            #     embed.add_field(name=name, value=value, inline=inline)
            # embed.set_author(name='{0.user}'.format(self), icon_url=self.guild.icon_url)
            # embed.set_footer(text="This is a footer")
            # await self.stdout.send(embed=embed)

            while not self.cogs_ready.all_ready():
                await sleep(0.5)
            
            self.ready = True
            print("Bot Ready")

        else:
            print("Bot Reconnect")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()