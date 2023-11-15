from nextcord.ext import commands
from nextcord import Message


class Afk(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return

        if message.mentions:
            for user in message.mentions:
                if user.id == message.author.id:
                    return
                if str(user.id) in self.client.afk:
                    await message.channel.send(
                        f"{user.mention} is currently AFK. Reason: {self.client.afk[str(user.id)]['reason']}"
                    )
                else:
                    return
        if str(message.author.id) in self.client.afk:
            afk_time = (
                message.created_at - self.client.afk[str(message.author.id)]["time"]
            )
            if afk_time.seconds <= 10:
                return
            del self.client.afk[str(message.author.id)]
            await message.channel.send(
                f"Welcome back {message.author.mention}! I removed your AFK status. You were AFK for {afk_time}"
            )

    @commands.command()
    @commands.has_any_role(
        866903831606067261,  # Head admin
        943534018564071555,  # Head admin badge
        822620759255154749,  # Admin
        822985879243980870,  # Moderator
        886171242422497312,  # Staff
        870814601254694942,  # Peeker (Level 20)
        905219932776710144,  # Helper
        897517045137178686,  # MVP
        863471477416394802,  # VIP
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def afk(self, ctx: commands.Context, *, reason: str = None):
        if reason is None:
            reason = "No reason provided"

        self.client.afk[str(ctx.author.id)] = {
            "reason": reason,
            "time": ctx.message.created_at,
        }
        await ctx.send(f"{ctx.author.mention} I set your AFK status. Reason: {reason}")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unafk(self, ctx: commands.Context):
        if str(ctx.author.id) in self.client.afk:
            afk_time = (
                ctx.message.created_at - self.client.afk[str(ctx.author.id)]["time"]
            )
            del self.client.afk[str(ctx.author.id)]
            await ctx.send(
                f"Welcome back {ctx.author.mention}! I removed your AFK status. You were AFK for {afk_time}"
            )
        else:
            await ctx.send(f"{ctx.author.mention} You are not AFK.")


def setup(client: commands.Bot):
    client.add_cog(Afk(client))
