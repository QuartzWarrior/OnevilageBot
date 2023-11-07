from nextcord.ext import commands, application_checks
from nextcord import (
    Interaction,
    ui,
    ButtonStyle,
    PartialEmoji,
    slash_command,
    RawReactionActionEvent,
    Embed,
    HTTPException,
    SlashOption,
)
from nextcord.abc import GuildChannel


class PersistentNotifs(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(
        label="YouTube Notifs",
        style=ButtonStyle.red,
        custom_id="persistent_view:yt_notif",
        emoji=PartialEmoji(name="🔥"),
    )
    async def yt_notifs(self, button: ui.Button, interaction: Interaction):
        role = await interaction.guild.get_role(863303717229953024)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(
                "Removed YouTube Notifications role. ", ephemeral=True
            )
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                "Added YouTube Notifications role. ", ephemeral=True
            )

    @ui.button(
        label="Events",
        style=ButtonStyle.blurple,
        custom_id="persistent_view:event",
        emoji=PartialEmoji(name="🎂"),
    )
    async def events(self, button: ui.Button, interaction: Interaction):
        role = await interaction.guild.get_role(894775200888029214)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(
                "Removed Events role. ", ephemeral=True
            )
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                "Added Events role. ", ephemeral=True
            )

    @ui.button(
        label="Chat Revival",
        style=ButtonStyle.grey,
        custom_id="persistent_view:chat_revive",
        emoji=PartialEmoji(name="🗿"),
    )
    async def chat_revival(self, button: ui.Button, interaction: Interaction):
        role = await interaction.guild.get_role(885348135013089310)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(
                "Removed Chat Revival role. ", ephemeral=True
            )
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                "Added Chat Revival role. ", ephemeral=True
            )

    @ui.button(
        label="Announcments",
        style=ButtonStyle.red,
        custom_id="persistent_view:announce",
        emoji=PartialEmoji(name="🔊"),
    )
    async def announcement(self, button: ui.Button, interaction: Interaction):
        role = await interaction.guild.get_role(878411750578466816)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(
                "Removed Announcments role. ", ephemeral=True
            )
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                "Added Announcments role. ", ephemeral=True
            )


class RRButtons(commands.Cog):
    def __init__(self, client: commands.Bot):
        super().__init__(client)
        self.client.persistent_views_added = False

    @commands.Cog.listener()
    async def on_ready(self, client):
        if not self.client.persistent_views_added:
            # Register the persistent view for listening here.
            # Note that this does not send the view to any message.
            # To do that, you need to send a message with the View as shown below.
            # If you have the message_id you can also pass it as a keyword argument, but for this example
            # we don't have one.
            self.client.add_view(PersistentNotifs())
            self.client.persistent_views_added = True

        print(f"Logged in as {self.client.user} (ID: {self.client.user.id})")

    @slash_command(guild_ids=[822525128306196500])
    @application_checks.has_any_role(822620759255154749, 935239717870518302)
    async def prepare(self, ctx):
        """Starts a persistent view."""
        # In order for a persistent view to be listened to, it needs to be sent to an actual message.
        # Call this method once just to store it somewhere.
        # In a more complicated program you might fetch the message_id from a database for use later.
        # However this is outside of the scope of this simple example.
        await ctx.delete()
        await ctx.send("Choose your notification roles", view=PersistentNotifs())


def setup(client):
    client.add_cog(RRButtons(client))


class ReactionRoles(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

        self.client.colour_roles = [
            868270208010321980,
            868270401313202207,
            868270434716643388,
            868270271352688690,
            914403045381660743,
            868270472561827870,
            868270315225120828,
        ]

        self.client.role_message_id = [
            972570121723846756,
            971566701000925255,
            971566807473328208,
        ]  # ID of the message that can be reacted to to add/remove a role.
        self.client.emoji_to_role = {
            PartialEmoji(name="🔴"): 868270208010321980,
            PartialEmoji(name="🔵"): 868270401313202207,
            PartialEmoji(name="🟣"): 868270434716643388,
            PartialEmoji(name="🟤"): 868270271352688690,
            PartialEmoji(
                name="64pxLocation_dot_cyan", id=914405545996345434
            ): 914403045381660743,
            PartialEmoji(name="PinkDot", id=913198449573371924): 868270472561827870,
            PartialEmoji(name="🟢"): 868270315225120828,
            PartialEmoji(name="🔥"): 863303717229953024,
            PartialEmoji(name="🎂"): 894775200888029214,
            PartialEmoji(name="🗿"): 885348135013089310,
            PartialEmoji(name="🔊"): 878411750578466816,
            PartialEmoji(name="💰"): 892098906840793118,
            PartialEmoji(name="💵"): 892098717736390717,
            PartialEmoji(name="nqn", id=906646908062289980): 892099032086880326,
        }

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        """Gives a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id not in self.client.role_message_id:
            return

        guild = self.client.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.client.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)

        for mrole in payload.member.roles:
            if mrole.id in self.client.colour_roles:
                await payload.member.remove_roles(mrole)

        if role is None:
            # Make sure the role still exists and is valid.
            return

        try:
            # Finally, add the role.
            await payload.member.add_roles(role)
        except HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        """Removes a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id not in self.client.role_message_id:
            return

        guild = self.client.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.client.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        # The payload for `on_raw_reaction_remove` does not provide `.member`
        # so we must get the member ourselves from the payload's `.user_id`.
        member = guild.get_member(payload.user_id)
        if member is None:
            # Make sure the member still exists and is valid.
            return

        try:
            # Finally, remove the role.
            await member.remove_roles(role)
        except HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

    @slash_command(guild_ids=[822525128306196500])
    @application_checks.has_any_role(822620759255154749, 935239717870518302)
    async def embed(
        self,
        interaction: Interaction,
        title: str = SlashOption(),
        description: str = SlashOption(),
        author: str = SlashOption(description="Author Name", required=False),
        authorurl: str = SlashOption(description="Author URL", required=False),
        footer: str = SlashOption(description="Footer Text", required=False),
        footericon: str = SlashOption(description="Footer Icon URL", required=False),
        image: str = SlashOption(required=False),
        thumbnail: str = SlashOption(required=False),
    ):
        # , color: str = SlashOption(description="The color you want", choices={"blue": "0x3498db", "blurple": "0x5865F2", "brand green": "0x57F287", "brand red": "0xED4245", "dark blue": "0x206694", "dark gold": "0xc27c0e", "dark gray": "0x607d8b", "dark green": "0x1f8b4c", "dark magenta": "0xad1457", "dark orange": "0xa84300", "dark purple": "0x71368a", "dark red": "0x992d22", "dark teal": "0x11806a", "dark theme": "0x36393F", "darker gray": "0x546e7a", "fuchsia": "0xEB459E", "gold": "0xf1c40f", "green": "0x2ecc71", "greyple": "0x99aab5", "light gray": "0x979c9f", "lighter gray": "0x95a5a6", "magenta": "0xe91e63", "old blurple": "0x7289da", "orange": "0xe67e22", "purple": "0x9b59b6", "red": "0xe74c3c", "teal": "0x1abc9c", "yellow": "0xFEE75C"})
        embed = Embed(title=title, description=str(description).replace("\n", "\n"))
        ok = embed.set_author(name=author, url=authorurl) if author else None
        ok = embed.set_footer(text=footer, icon_url=footericon) if footer else None
        ok = embed.set_image(url=image) if image else None
        ok = embed.set_thumbnail(url=thumbnail) if thumbnail else None
        await interaction.response.send_message(embed=embed)

    @slash_command(guild_ids=[822525128306196500])
    @application_checks.has_any_role(822620759255154749, 935239717870518302)
    async def rrembeds(
        self,
        interaction: Interaction,
        channel: GuildChannel = SlashOption(),
    ):
        embed = Embed(
            title="Your name will be displayed based on the colour you choose",
            description="""            
➤ Red : :red_circle:

➤ Blue : :blue_circle:

➤ Green : :green_circle:

➤ Cyan : :64pxLocation_dot_cyan:

➤ Brown : :brown_circle:

➤ Purple : :purple_circle:

➤ Pink : :PinkDot:
                               """,
        )
        embed.set_image(
            url="https://c.tenor.com/7yoCzFbvNR4AAAAC/color-roles-roles.gif"
        )
        embed.set_author(name="Colour Roles")
        msg = await channel.send(embed=embed)
        print(msg.id)
        embed = Embed(
            title="Notifications:",
            descriptiom="""》Youtube notification ping : 🔥

》Event ping : 🎂

》Chat revival ping : 🗿

》Announcement ping : 🔊""",
        )
        msg = await channel.send(embed=embed)
        print(msg.id)
        embed = Embed(
            title="",
            description="""》Dank coin giveaway : 💰

》Robux giveaway : 💵

》Other giveaway : :nqn:""",
        )
        msg = await channel.send(embed=embed)
        print(msg.id)


def setup(client):
    client.add_cog(ReactionRoles(client))
