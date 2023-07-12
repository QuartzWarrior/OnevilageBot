import nextcord
from nextcord.ext import commands, application_checks
from nextcord.ext.commands.errors import MissingPermissions, CommandNotFound
from datetime import timedelta, datetime
from decimal import Decimal
from googleapiclient import discovery
class ModerationMenu(nextcord.ui.View):
    def __init__(self, message, user):
        super().__init__()
        self.message = message   
        self.user = user
    @nextcord.ui.button(label='Ban', style=nextcord.ButtonStyle.danger)
    async def ban_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        button.disabled = True
        await self.user.ban()
        await interaction.response.send_message('Succesfully banned.', ephemeral=True)
    @nextcord.ui.button(label='Kick', style=nextcord.ButtonStyle.primary)
    async def kick_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        button.disabled = True
        await self.user.kick()
        await interaction.response.send_message('Succesfully kicked.', ephemeral=True)
    @nextcord.ui.button(label='Mute', style=nextcord.ButtonStyle.primary)
    async def mute_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.user.timeout(timeout=timedelta(days=1))
        await interaction.response.send_message(f'Succesfully muted {self.user} for 1 day.', ephemeral=True)
    async def interaction_check(self, interaction):
        if interaction.user != self.message.author:
            return False
        elif interaction.user.top_role.position < self.user.top_role.position:
            return False
        else:
            return True
    async def on_error(self, error, item, interaction):
        await interaction.response.defer()
        exception = '\n'.join(traceback.format_exception(type(error), error, error.__traceback__))
        exception = f'```py\n{exception}```'
        await interaction.channel.send(f'An error occured in the button `{item.custom_id}`:\n{exception}')


class Moderation(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.snipe_dict = {}
        self.edit_dict = {}
        self.reaction_dict = {}

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        try:
            if self.reaction_dict[payload.channel_id] == "Pyth0nC0de":
                self.reaction_dict[payload.channel_id] = f"{payload.emoji.name}Pyth0nC0de{payload.user_id}Pyth0nC0de{payload.emoji.url}"
            elif ("Pyth0nC0de" in self.reaction_dict[payload.channel_id]) or ("Pyth0nC0d3" in self.reaction_dict[payload.channel_id]):
                if "Pyth0nC0d3" in self.reaction_dict[payload.channel_id] and len(self.reaction_dict[payload.channel_id].split("Pyth0nC0d3")) >= 2:
                    temp = self.reaction_dict[payload.channel_id].split("Pyth0nC0d3")
                    temp.pop(0)
                    self.reaction_dict[payload.channel_id] = "Pyth0nC0d3".join(temp)
                self.reaction_dict[payload.channel_id] = self.reaction_dict[payload.channel_id] + f"Pyth0nC0d3{payload.emoji.name}Pyth0nC0de{payload.user_id}Pyth0nC0de{payload.emoji.url}"
        except KeyError:
            self.reaction_dict[payload.channel_id] = f"{payload.emoji.name}Pyth0nC0de{payload.user_id}Pyth0nC0de{payload.emoji.url}"
        channel = self.client.get_channel(self.LOG_CHANNEL_ID)
        user = self.client.get_user(payload.user_id)
        embed = nextcord.Embed(title="Reaction Removed", description=f"Removed by {user}")
        embed.add_field(name="Emoji",value=f":{payload.emoji.name}:")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.client.get_channel(self.LOG_CHANNEL_ID)
        embed = nextcord.Embed(title="Reaction Added", description=f"Added by {payload.member}")
        embed.add_field(name="Emoji",value=f":{payload.emoji.name}:")
        await channel.send(embed=embed)

    @commands.command()
    @commands.has_any_role(866903831606067261, 822620759255154749, 822985879243980870, 886171242422497312, 919433872368869436, 905219932776710144, 897517045137178686, 935239717870518302)
    async def rs(self, message):
        try:
            if self.reaction_dict[message.channel.id] == "Pyth0nC0de":
                await message.send("No reactions to snipe!", delete_after=3)
            elif "Pyth0nC0d3" in self.reaction_dict[message.channel.id] and self.reaction_dict[message.channel.id] != "Pyth0nC0d3":
                embeds = []
                multiple = self.reaction_dict[message.channel.id].split("Pyth0nC0d3")
                for data in multiple:
                    split_data = data.split("Pyth0nC0de")
                    user = self.client.get_user(int(split_data[1]))
                    embed = nextcord.Embed(title=f"Deleted Reaction", description=f":{split_data[0]}:")
                    embed.set_author(name=str(user), icon_url=user.display_avatar)
                    if split_data[-1] != "":
                        embed.set_thumbnail(url=split_data[-1])
                    embeds.append(embed)
                await message.send(embeds=embeds)
            elif "Pyth0nC0de" in self.reaction_dict[message.channel.id] and self.reaction_dict[message.channel.id] != "Pyth0nC0de":
                split_data = self.reaction_dict[message.channel.id].split("Pyth0nC0de")
                user = message.guild.get_member(int(split_data[1]))
                embed = nextcord.Embed(title=f"Deleted Reaction", description=f":{split_data[0]}:")
                embed.set_author(name=str(user), icon_url=user.display_avatar)
                if split_data[-1] != "":
                    embed.set_thumbnail(url=split_data[-1])
                await message.send(embed=embed)
            self.reaction_dict[message.channel.id] = "Pyth0nC0de"
        except KeyError:
            await message.send("No reactions to snipe!", delete_after=3)


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content != after.content and not (before.author.id in [986315141308121129, 946434857368698920]):
            try:
                if len(self.edit_dict[before.channel.id]) >= 2:
                    self.edit_dict[before.channel.id].pop(0)
                self.edit_dict[before.channel.id].append({"before": str(before.content), "after": str(after.content), "author": before.author.id, "created": before.created_at})
        
            except KeyError:
                self.edit_dict[before.channel.id] = []
                self.edit_dict[before.channel.id].append({"before": str(before.content), "after": str(after.content), "author": before.author.id, "created": before.created_at})

    
    @commands.command(aliases=['esnipe', 'editsnipe', 'snipeedit'])
    @commands.has_any_role(897517045137178686, 935239717870518302, 919433872368869436, 905219932776710144,
                           822985879243980870, # Mod
                           822620759255154749) # Admin
    async def es(self, com_message):
        try:
            data = self.edit_dict[com_message.channel.id]
        except KeyError:
            await com_message.send("No messages to snipe!", delete_after=3)
            return
        if len(data) > 0:
            embeds = []
            for message in data:
                author = com_message.guild.get_member(message["author"])
                embed = nextcord.Embed(title=f"Edited Message", timestamp=message["created"])
                embed.add_field(name="Before: ", value=message["before"])
                embed.add_field(name="After: ", value=message["after"])
                embed.set_author(name=str(author), icon_url=author.display_avatar)
                embeds.append(embed)
            await com_message.send(embeds=embeds)
            self.edit_dict[com_message.channel.id] = []
        else:
            await com_message.send("No messages to snipe!", delete_after=3)


    # Alternative sniping method
    #@commands.Cog.listener()
    #async def on_message_delete(self, message):
    #  if message.author.bot:
    #    return
    #  self.last_deleted = message.content
    #  self.deleted_author = message.author
    #  self.createdAt = message.created_at
    #  self.img = str(message.attachments[0].url) if message.attachments else 'No'

    
    # Current method
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id == self.client.user.id:
            return
        if (message.content or message.attachments) and not (message.author.id in [986315141308121129, 946434857368698920]):
            try:
                if len(self.snipe_dict[message.channel.id]) >= 2:
                    self.snipe_dict[message.channel.id].pop(0)
                self.snipe_dict[message.channel.id].append({"content": message.content, "author": message.author.id, "created": message.created_at, "attachments": message.attachments})

            except KeyError:
                self.snipe_dict[message.channel.id] = []
                self.snipe_dict[message.channel.id].append({"content": message.content, "author": message.author.id, "created": message.created_at, "attachments": message.attachments})


    @commands.command(aliases=['s'])
    @commands.has_any_role(866903831606067261, 822620759255154749, 822985879243980870, 886171242422497312, 919433872368869436, 905219932776710144, 897517045137178686, 935239717870518302, 1054451727841116240)
    async def snipe(self, com_message):
        try:
            data = self.snipe_dict[com_message.channel.id]
        except KeyError:
            await com_message.send("No messages to snipe!", delete_after=3)
            return
        if len(data) > 0:
            error = None
            embeds = []
            attachments = []
            files = []
            for message in data:
                if message["attachments"]:
                    attachments.extend(message["attachments"])
                author = com_message.guild.get_member(message["author"])
                embed = nextcord.Embed(title=f"Deleted Message", description=message["content"], timestamp=message["created"])
                try:
                    embed.set_author(name=str(author), icon_url=author.display_avatar)
                except:
                    pass
                embeds.append(embed)
            for attachment in attachments:
                try:
                    files.append(await attachment.to_file(use_cached=True))
                except nextcord.errors.NotFound:
                    error = "404 Not Found (error code: 0): asset not found"
                except nextcord.errors.HTTPException:
                    error = "415 Unsupported Media Type (error code: 0): failed to get asset"
            if files:
                await com_message.send(content=error, embeds=embeds, files=files)
            else:
                await com_message.send(content=error, embeds=embeds)
            self.snipe_dict[com_message.channel.id] = []
        else:
            await com_message.send("No messages to snipe!", delete_after=3)


    # Alternative sniping method
    #@commands.Cog.listener()
    #async def on_message_delete(self, message):
    #  if message.author.bot:
    #    return
    #  self.last_deleted = message.content
    #  self.deleted_author = message.author
    #  self.createdAt = message.created_at
    #  self.img = str(message.attachments[0].url) if message.attachments else 'No'

    
    # Current method
    @commands.Cog.listener()
    async def on_message_deleted(self, message):
        if message.embeds != []:
            channel = self.client.get_channel(self.LOG_CHANNEL_ID)
            await channel.send(content=f"Deleted Embed in <#{message.channel.id}> from {message.author}", embeds=message.embeds)
        id = message.channel

        cont = message.content if message.content != '' else '*No Content*'
        
        atta = "No"
        
        if message.attachments:
            atta = ""
            for attchmnt in message.attachments:
                atta += attchmnt.url if atta == "" else str("!$)($!" + attchmnt.url)
        
        if atta == "No" and cont == "*No Content*":
            return
        
        msg = str(cont) + '˙' + str(message.author) + '˙' + str(message.author.display_avatar) + '˙' + str(message.created_at) + '˙' + str(atta) + ''
        try:
            e=self.snipe_dict[id]
        except KeyError:
            self.snipe_dict[id] = ''
        new_snip_dict = self.snipe_dict[id].replace("Pyth0nC0de", "")
        self.snipe_dict[id] = new_snip_dict + "`~=/" + msg

    @commands.command(name='modsnipe', aliases=['mods'], hidden=True)
    @commands.has_guild_permissions(manage_messages=True)
    async def multisniped(self, ctx):
        try:
            id = ctx.message.channel
            wow = self.snipe_dict[id]
        except KeyError:
            await ctx.send("There's nothing to snipe!")
        if self.snipe_dict[id] == 'Pyth0nC0de':
            await ctx.send('There\'s nothing to snipe!')
        else:
            snip_count = 0
            snippps = wow.split("`~=/").reverse()
            for snippp in snippps:
                try:
                    msg, auth, avatar, createdAt, img = snippp.split('˙')
                except ValueError:
                    pass
                else:
                    snip_count += 1
                    if snip_count == 10:
                        return
                    embed = nextcord.Embed(title='Deleted Message', color=nextcord.Colour.random(), timestamp=datetime.fromisoformat(createdAt))
                    embed.add_field(name=auth, value=msg, inline=False)
                    embed.set_thumbnail(url=avatar)
                    embeds = [embed]
                    if img != "No":
                        imgs = img.split('!$)($!')
                        if len(imgs) == 1:
                            embed.set_image(url=imgs[0])
                        else:
                            embeds = [embed]
                            for atta in imgs:
                                embeds.append(nextcord.Embed(colour=nextcord.Colour.random()).set_image(url=atta))
                    await ctx.send(embeds=embeds)
            self.snipe_dict[id] = 'Pyth0nC0de'

            #print(self.snipe_dict)

    @commands.command(hidden=True)
    async def sniped(self, ctx):
        try:
            id = ctx.message.channel
            wow = self.snipe_dict[id]
        except KeyError:
            await ctx.send("There's nothing to snipe!")
        if self.snipe_dict[id] == 'Pyth0nC0de':
            await ctx.send('There\'s nothing to snipe!')
        else:
            snip_count = 0
            for snippp in wow.split("`~=/"):
                try:
                    msg, auth, avatar, createdAt, img = wow.split("`~=/")[-1].split('˙')
                except ValueError:
                    pass
                else:
                    snip_count += 1
                    if snip_count == 2:
                        return
                    embed = nextcord.Embed(title='Deleted Message', color=nextcord.Colour.random(), timestamp=datetime.fromisoformat(createdAt))
                    embed.add_field(name=auth, value=msg, inline=False)
                    embed.set_thumbnail(url=avatar)
                    embeds = [embed]
                    if img != "No":
                        imgs = img.split('!$)($!')
                        if len(imgs) == 1:
                            embed.set_image(url=imgs[0])
                        else:
                            embeds = [embed]
                            for atta in imgs:
                                embeds.append(nextcord.Embed(colour=nextcord.Colour.random()).set_image(url=atta))
                    await ctx.send(embeds=embeds)
            self.snipe_dict[id] = wow.replace(wow.split("`~=/")[-1], "")


    @commands.command(aliases=["clean"], description="Cleans a certian amount of messages.")
    @commands.has_guild_permissions(manage_messages=True)
    async def Purge(self, message, limit: int=None):
        if limit is None:
            await message.send("Correct usage is `o!Purge <user>`")
        else:
            try:
                await message.channel.purge(limit=limit + 1)
                await message.send(f"{limit} messages have been deleted.", delete_after=3)
            except MissingPermissions:
                await message.send("You have insufficient permissions to do this command.")


    @commands.command()
    @commands.has_guild_permissions(moderate_members=True)
    async def Mute(self, message, user: nextcord.Member = None, reason: str = None, days: int = 1, hours: int = 0, minutes: int = 0):
        if user is None:
            await message.send("Correct usage is `o!Mute [user] <reason> <days:1> <hours:0> <minutes:0>`")
        else:
            if message.author.top_role.position < user.top_role.position:
                await message.send("You cannot mute someone a higher rank than you.")
            else:
                await user.timeout(timeout=timedelta(days=days, hours=hours, minutes=minutes), reason=reason)
                await message.send(f"Succesfully muted {user} for {days} day(s), {hours} hour(s), and {minutes} minute(s). Reason: {reason}.")


    @commands.command()
    @commands.has_guild_permissions(moderate_members=True)
    async def Unmute(self, message, user: nextcord.Member = None, reason: str = None):
        if user is None:
            await message.send("Correct usage is `o!Unmute [user] <reason>`")
        else:
            await user.timeout(timeout=None, reason=reason)
            await message.send(f"Successfully unmuted {user}. Reason: {reason}.")


    @commands.command()
    @commands.has_guild_permissions(kick_members=True)
    async def Kick(self, message, user: nextcord.Member=None, *, reason=None):
        if user is None:
            await message.send("Correct usage is `o!Kick <user>`")
        else:
            try:
                embed=nextcord.Embed(title=f"You have been kicked from {message.guild}.",description="")
                embed.add_field(name="Reason",value=reason)
                await user.send(embed=embed)
            except MissingPermissions:
                await message.send("You have insufficient permissions to do this command.")
            except nextcord.errors.HTTPException:
                await message.send("Cannot send messages to this user.", delete_after=3)
            await user.kick(reason=reason)
            await message.send(f"{user.name} has been kicked.")


    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    async def Ban(self, message, user: nextcord.Member=None, *, reason=None):
        if user is None:
            await message.send("Correct usage is `o!Ban <user>`")
        else:
            try:
                embed=nextcord.Embed(title=f"You have been banned from {message.guild}.",description="")
                embed.add_field(name="Reason",value=reason)
                await user.send(embed=embed)
            except MissingPermissions:
                await message.send("You have insufficient permissions to do this command.")
            except nextcord.errors.HTTPException:
                await message.send("Cannot send messages to this user.", delete_after=3)
            await user.ban(reason=reason)
            await message.send(f"{user.name} has been banned.")


    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    async def Unban(self, message, *, user=None):
        if user is None:
            await message.send("Correct usage is `o!Unban <user>`")
        else:
            try:
                banned_users = await message.guild.bans()
                member_name, member_discriminator = user.split('#')

                for ban_entry in banned_users:
                    user = ban_entry.user
            
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await message.guild.unban(user)
                    await message.send(f"{user} has been unbanned.")
                    return
            except MissingPermissions:
                await message.send("You have insufficient permissions to do this command.")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def member(self, message, member: nextcord.Member):
        embed=nextcord.Embed(title=f"About {member.name}", description="")
        embed.set_thumbnail(url=member.display_avatar)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Joined at", value=member.joined_at)
        embed.add_field(name="Created at",value=member.created_at)
        await message.send(embed=embed, view=ModerationMenu(message, member))


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, message, channel: nextcord.TextChannel=None):
        if channel is None:
            channel = message.channel
        everyone = message.guild.get_role(822525128306196500)
        member = message.guild.get_role(869270654191542313)
        image = message.guild.get_role(913451714399580280)
        embed = message.guild.get_role(913508354519883787)
        if channel.permissions_for(member).view_channel is False:
            pass
        else:
            await channel.set_permissions(everyone, send_messages=False)
            await channel.set_permissions(member, send_messages=False)
            await channel.set_permissions(image, send_messages=False)
            await channel.set_permissions(embed, send_messages=False)
        await message.send(f"Succesfully locked {channel}.")


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, message, channel: nextcord.TextChannel=None):
        if channel is None:
            channel = message.channel
        await channel.edit(sync_permissions=True, reason="Unlocked channel.")
        await message.send(f"Succesfully unlocked {channel}.")


    @commands.command(aliases=["sm"])
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, message, amount: int=None):
        if amount is None:
            await message.send("Correct usage is\n`o!slowmode <amount-in-seconds>`")
        else:
            await message.channel.edit(slowmode_delay=amount)
            await message.send(f"Sucessfully set the slowmode to {amount} in this channel.")


    @commands.command(aliases=["ann"])
    @commands.has_any_role(935239717870518302, 866903831606067261, 822620759255154749)
    async def announce(self, message, channel: nextcord.TextChannel, *, msg):
        await channel.send(msg)


    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')


    @commands.command()
    async def watchlist(self, ctx):
        roles = await ctx.guild.fetch_roles()
        full = []
        for role in roles:
            if role.id == 958480959685132318:
                for member in role.members:
                    full.append(str(member))
                await ctx.send("\n".join(full))
                return


    @nextcord.message_command(name="Hidden Message Analyser", guild_ids=[822525128306196500])
    @application_checks.has_permissions(manage_messages=True)
    async def hidden_msg_analyser(self, interaction: nextcord.Interaction, message):
        GOOGLE_API_KEY = self.GOOGLE_API_KEY
        #message = message

        cclient = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=GOOGLE_API_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
        )
        analyze_request = {
                  'comment': { 'text': message.content },
                  'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'IDENTITY_ATTACK': {}, 'INSULT': {}, 'PROFANITY': {}, 'THREAT': {}, 'SEXUALLY_EXPLICIT': {}, 'FLIRTATION': {}},

                  'languages': ["en"]
                }
        response = cclient.comments().analyze(body=analyze_request).execute()
        embed = nextcord.Embed(title="High check", description=f"Comment Analyzer: {message.content}\n\n[Jump to message]({message.jump_url})")
        values = [embed.add_field(name=attribute.lower().title().replace("_", " "), value=str(100*round(Decimal(float(response['attributeScores'][attribute]['summaryScore']['value'])), 2)) + "%") for attribute in response['attributeScores'].keys()]
        embed.set_thumbnail(url=message.author.display_avatar)
        await interaction.send(embed=embed, ephemeral=True)


    @nextcord.message_command(name="Message Analyser", guild_ids=[822525128306196500])
    @application_checks.has_permissions(manage_messages=True)
    async def msg_analyser(self, interaction: nextcord.Interaction, message):
        GOOGLE_API_KEY = self.GOOGLE_API_KEY
        #message = message

        cclient = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=GOOGLE_API_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
        )
        analyze_request = {
                  'comment': { 'text': message.content },
                  'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'IDENTITY_ATTACK': {}, 'INSULT': {}, 'PROFANITY': {}, 'THREAT': {}, 'SEXUALLY_EXPLICIT': {}, 'FLIRTATION': {}},

                  'languages': ["en"]
                }
        response = cclient.comments().analyze(body=analyze_request).execute()
        embed = nextcord.Embed(title="High check", description=f"Comment Analyzer: {message.content}\n\n[Jump to message]({message.jump_url})")
        values = [embed.add_field(name=attribute.lower().title().replace("_", " "), value=str(100*round(Decimal(float(response['attributeScores'][attribute]['summaryScore']['value'])), 2)) + "%") for attribute in response['attributeScores'].keys()]
        embed.set_thumbnail(url=message.author.display_avatar)
        await interaction.send(embed=embed, ephemeral=False)


    @Kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(title="Missing Permissions",description="You have insufficient permissions to do this command.", color=nextcord.Color.green())
            await ctx.send(embed=embed)


    @Ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(title="Missing Permissions",description="You have insufficient permissions to do this command.", color=nextcord.Color.green())
            await ctx.send(embed=embed)
        elif isinstance(error, nextcord.errors.HTTPException):
            embed = nextcord.Embed(title="HTTP Exception",description="Cannot send messages to this user.", color=nextcord.Color.green())
            await ctx.send(embed=embed)


    @Unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(title="Missing Permissions",description="You have insufficient permissions to do this command.", color=nextcord.Color.green())
            await ctx.send(embed=embed)


    @Mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(title="Missing Permissions",description="You have insufficient permissions to do this command.", color=nextcord.Color.green())
            await ctx.send(embed=embed)
            

    @slowmode.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(title="Missing Permissions",description="You have insufficient permissions to do this command.", color=nextcord.Color.green())
            await ctx.send(embed=embed)


    @Purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(title="Missing Permissions",description="You have insufficient permissions to do this command.", color=nextcord.Color.green())
            await ctx.send(embed=embed)


    @snipe.error
    async def sniped_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            embed = nextcord.Embed(title="Missing Roles",description=error, color=nextcord.Color.green())
            await ctx.send(embed=embed)


    @member.error
    async def member_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(title="Missing Permissions",description="You have insufficient permissions to do this command.", color=nextcord.Color.green())
            await ctx.send(embed=embed)
        elif isinstance(error, nextcord.ext.commands.errors.MissingRequiredArgument):
            embed = nextcord.Embed(title="Missing Required Argument", description=error, color = nextcord.Color.blurple())
            await ctx.send(embed=embed)


    @announce.error
    async def announce_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            embed = nextcord.Embed(title="Missing Permissions",description=error, color=nextcord.Color.green())
            await ctx.send(embed=embed)
        elif isinstance(error, nextcord.ext.commands.errors.MissingRequiredArgument):
            embed = nextcord.Embed(title="Missing Required Argument", description=error, color = nextcord.Color.blurple())
            await ctx.send(embed=embed)

            
def setup(client):
    client.add_cog(Moderation(client))