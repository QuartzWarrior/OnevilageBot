from os import system

from nextcord.ext import commands
from nextcord.ext.commands.errors import ExtensionNotFound, ExtensionNotLoaded, ExtensionAlreadyLoaded


class CogFunctions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True)
    async def disable(self, ctx, *, module):
        if ctx.author.id == 713512807580303440 or ctx.author.id == 802725022560944160 or ctx.author.id == 1065714439380271164:
            try:
                self.client.unload_extension(module.strip())
                await ctx.send(f"Disabled module: `{module}`")
            except ExtensionNotLoaded:
                await ctx.send(f"Module {module.strip()} is already disabled or doesn't exist")
        else:
            await ctx.send('You do not have permission to do this command.')

    @commands.command(hidden=True)
    async def enable(self, ctx, *, module):
        if ctx.author.id == 713512807580303440 or ctx.author.id == 802725022560944160 or ctx.author.id == 1065714439380271164:
            try:
                self.client.load_extension(module.strip())
                await ctx.send(f"Enabled module: `{module.strip()}`")
            except ExtensionAlreadyLoaded:
                await ctx.send(f"Module `{module.strip()}` is already enabled")
            except ExtensionNotFound:
                await ctx.send(f"Module `{module.strip()}` doesn't exist")
        else:
            await ctx.send('You do not have permission to do this command.')

    @commands.command(hidden=True)
    async def reload(self, message, *, module):
        if message.author.id == 713512807580303440 or message.author.id == 802725022560944160 or message.author.id == 1065714439380271164:
            try:
                self.client.reload_extension(module.strip())
                await message.send(f"Reloaded module: `{module}`")
            except ExtensionNotFound:
                await message.send(f"Module `{module.strip()}` doesn't exist")
            except ExtensionNotLoaded:
                await message.send(f"Module {module.strip()} is already disabled or doesn't exist")
        else:
            await message.send(
                "You do not have permission to do this command. Contact `QuartzWarrior#9250` if this is an error.")


    @commands.command(hidden=True)
    async def restart(self, ctx):
        if ctx.author.id == 713512807580303440:
            try:
                await self.close()
            except:
                pass
            finally:
                system("python3 main.py")


def setup(client):
    client.add_cog(CogFunctions(client))
