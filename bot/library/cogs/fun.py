from discord import Member
from typing import Optional
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import BadArgument
from discord.ext.commands import command, cooldown
from random import choice, randint 

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="test", aliases=["testcommand", "tc"])
    async def test(self, ctx):
        pass

    @command(name="hello", aliases=["hi"])
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hello', 'Hi', 'Hey', 'Hiya'))} {ctx.author.mention}!")

    @command(name="dice", aliases=["roll"])
    async def roll_dice(self, ctx, die_string: str):
        dice, value = (int(term) for term in die_string.split("d"))
        if dice <= 25:
            rolls = [randint(1, value) for i in range(dice)]
            await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")
        else:
            await ctx.send("I can't roll that many dice. Please try a lower number.")

    @command(name="slap", aliases=["hit"])
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "for no reason"):
        await ctx.send(f"{ctx.author.mention} slapped {member.mention} {reason}!")

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
	    if isinstance(exc, BadArgument):
		    await ctx.send("I can't find that member.")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Fun")

    

def setup(bot):
    bot.add_cog(Fun(bot))