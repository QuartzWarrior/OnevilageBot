from googleapiclient import discovery
from decimal import Decimal
from logging import getLogger, INFO, FileHandler, Formatter
from nextcord import ui, Embed, ButtonStyle, Colour, utils, PartialEmoji, Interaction, Color, Intents

GOOGLE_API_KEY = '' # Insert your perspective api key to enable message scanning

CLARIFAI_API_KEY = '' # OLD, don't need

LOG_CHANNEL_ID = 0

TOKEN = ''

cclient = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=GOOGLE_API_KEY,
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)

persistent_views_added = False

logger = getLogger('nextcord')
logger.setLevel(INFO)
handler = FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
from nextcord.ext import commands
from nextcord.ext.commands.errors import MissingPermissions, CommandNotFound


class VerifyMenu(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @ui.button(label='Verify', style=ButtonStyle.blurple, custom_id='verifymenu:verify')
    async def verify_callback(self, button, interaction):
        role = interaction.guild.get_role(869270654191542313)
        await interaction.user.add_roles(role)
        role1 = interaction.guild.get_role(897132880214491146)
        await interaction.user.remove_roles(role1)
        channel = client.get_channel(LOG_CHANNEL_ID)
        if not channel:
            return
        await channel.send(embed=Embed(title=" ", description=f"Changed roles for {interaction.user.name}#{interaction.user.discriminator}, +Member, -Unverified", color = Colour.green()))
        await interaction.response.send_message('Succesfully verified.', ephemeral=True)
    async def interaction_check(self, interaction):
        role = utils.get(interaction.guild.roles, name="Member")
        if role in interaction.user.roles:
            role1 = utils.get(interaction.guild.roles, name="Unverified")
            if role1 in interaction.user.roles:
                await interaction.user.remove_roles(role1)
            return False
        else:
            return True


class PersistentColours(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.colour_roles = [868270208010321980, 868270401313202207, 868270434716643388, 868270271352688690, 914403045381660743, 868270472561827870, 868270315225120828]    
        
    @ui.button(label='Red', style=ButtonStyle.red, custom_id='persistent_view:red', emoji=PartialEmoji(name='🔴'))
    async def red(self, button: ui.Button, interaction: Interaction):
        role = interaction.guild.get_role(868270208010321980)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message('Removed Red role. ', ephemeral=True)
        else:
            for mrole in interaction.user.roles:
                if mrole.id in self.colour_roles:
                    await interaction.user.remove_roles(mrole)
            await interaction.user.add_roles(role)
            await interaction.response.send_message('Added Red role. ', ephemeral=True)
            
    @ui.button(label='Brown', style=ButtonStyle.gray, custom_id='persistent_view:brown', emoji=PartialEmoji(name='🟤'))
    async def brown(self, button: ui.Button, interaction: Interaction):
        role = interaction.guild.get_role(868270271352688690)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message('Removed Brown role. ', ephemeral=True)
        else:
            for mrole in interaction.user.roles:
                if mrole.id in self.colour_roles:
                    await interaction.user.remove_roles(mrole)
            await interaction.user.add_roles(role)
            await interaction.response.send_message('Added Brown role. ', ephemeral=True)
            
    @ui.button(label='Purple', style=ButtonStyle.grey, custom_id='persistent_view:purple', emoji=PartialEmoji(name='🟣'))
    async def purple(self, button: ui.Button, interaction: Interaction):
        role = interaction.guild.get_role(868270434716643388)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message('Removed Purple role. ', ephemeral=True)
        else:
            for mrole in interaction.user.roles:
                if mrole.id in self.colour_roles:
                    await interaction.user.remove_roles(mrole)
            await interaction.user.add_roles(role)
            await interaction.response.send_message('Added Purple role. ', ephemeral=True)
            
    @ui.button(label='Blue', style=ButtonStyle.blurple, custom_id='persistent_view:blue', emoji=PartialEmoji(name='🔵'))
    async def blue(self, button: ui.Button, interaction: Interaction):
        role = interaction.guild.get_role(868270401313202207)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message('Removed Blue role. ', ephemeral=True)
        else:
            for mrole in interaction.user.roles:
                if mrole.id in self.colour_roles:
                    await interaction.user.remove_roles(mrole)
            await interaction.user.add_roles(role)
            await interaction.response.send_message('Added Blue role. ', ephemeral=True)
            
    @ui.button(label='Cyan', style=ButtonStyle.blurple, custom_id='persistent_view:cyan', emoji=PartialEmoji(name='64pxLocation_dot_cyan', id=914405545996345434))
    async def cyan(self, button: ui.Button, interaction: Interaction):
        role = interaction.guild.get_role(914403045381660743)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message('Removed Cyan role. ', ephemeral=True)
        else:
            for mrole in interaction.user.roles:
                if mrole.id in self.colour_roles:
                    await interaction.user.remove_roles(mrole)
            await interaction.user.add_roles(role)
            await interaction.response.send_message('Added Cyan role. ', ephemeral=True)
            
    @ui.button(label='Pink', style=ButtonStyle.red, custom_id='persistent_view:pink', emoji=PartialEmoji(name='PinkDot', id=913198449573371924))
    async def pink(self, button: ui.Button, interaction: Interaction):
        role = interaction.guild.get_role(868270472561827870)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message('Removed Pink role. ', ephemeral=True)
        else:
            for mrole in interaction.user.roles:
                if mrole.id in self.colour_roles:
                    await interaction.user.remove_roles(mrole)
            await interaction.user.add_roles(role)
            await interaction.response.send_message('Added Pink role. ', ephemeral=True)
            
    @ui.button(label='Green', style=ButtonStyle.green, custom_id='persistent_view:green', emoji=PartialEmoji(name='🟢'))
    async def green(self, button: ui.Button, interaction: Interaction):
        role = interaction.guild.get_role(868270315225120828)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message('Removed Green role. ', ephemeral=True)
        else:
            for mrole in interaction.user.roles:
                if mrole.id in self.colour_roles:
                    await interaction.user.remove_roles(mrole)
            await interaction.user.add_roles(role)
            await interaction.response.send_message('Added Green role. ', ephemeral=True)
        
        
class PersistentNotifs(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label='YouTube Notifs', style=ButtonStyle.red, custom_id='persistent_view:yt_notif', emoji=PartialEmoji(name='🔥'))
    async def yt_notifs(self, button: ui.Button, interaction: Interaction):
        role = interaction.guild.get_role(863303717229953024)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message('Removed YouTube Notifications role. ', ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message('Added YouTube Notifications role. ', ephemeral=True)

    @ui.button(label='Events', style=ButtonStyle.blurple, custom_id='persistent_view:event', emoji=PartialEmoji(name='🎂'))
    async def events(self, button: ui.Button, interaction: Interaction):
        role = interaction.guild.get_role(894775200888029214)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message('Removed Events role. ', ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message('Added Events role. ', ephemeral=True)

    @ui.button(label='Chat Revival', style=ButtonStyle.grey, custom_id='persistent_view:chat_revive', emoji=PartialEmoji(name='🗿'))
    async def chat_revival(self, button: ui.Button, interaction: Interaction):
        role = interaction.guild.get_role(885348135013089310)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message('Removed Chat Revival role. ', ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message('Added Chat Revival role. ', ephemeral=True)
            
    @ui.button(label='Announcments', style=ButtonStyle.red, custom_id='persistent_view:announce', emoji=PartialEmoji(name='🔊'))
    async def announcement(self, button: ui.Button, interaction: Interaction):
        role = interaction.guild.get_role(878411750578466816)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message('Removed Announcments role. ', ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message('Added Announcments role. ', ephemeral=True)


class PersistentGiveaways(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label='Dank Coins', style=ButtonStyle.red, custom_id='persistent_view:dankcoin', emoji=PartialEmoji(name='💰'))
    async def dankcoins(self, button: ui.Button, interaction: Interaction):
        role = interaction.guild.get_role(892098906840793118)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message('Removed Dank Coins Giveaway role. ', ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message('Added Dank Coins Giveaway role. ', ephemeral=True)
            
    @ui.button(label='Robux', style=ButtonStyle.gray, custom_id='persistent_view:robuxgiveaway', emoji=PartialEmoji(name='💵'))
    async def rbxgive(self, button: ui.Button, interaction: Interaction):
        role = interaction.guild.get_role(892098717736390717)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message('Removed Robux Giveaways role. ', ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message('Added Robux Giveaways role. ', ephemeral=True)
            
    @ui.button(label='Other', style=ButtonStyle.blurple, custom_id='persistent_view:other', emoji=PartialEmoji(name='nqn', id=906646908062289980))
    async def othernqn(self, button: ui.Button, interaction: Interaction):
        role = interaction.guild.get_role(892098906840793118)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message('Removed Other Giveaways role. ', ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message('Added Other Giveaways role. ', ephemeral=True)
            
            
class Client(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.persistent_views_added = False
        self.colour_roles = [868270208010321980, 868270401313202207, 868270434716643388, 868270271352688690, 914403045381660743, 868270472561827870, 868270315225120828]

    async def on_ready(self):
        if not self.persistent_views_added:
            # Register the persistent view for listening here.
            # Note that this does not send the view to any message.
            # To do that, you need to send a message with the View as shown below.
            # If you have the message_id you can also pass it as a keyword argument, but for this example
            # we don't have one.
            self.add_view(PersistentNotifs())
            self.add_view(VerifyMenu())
            self.add_view(PersistentGiveaways())
            self.add_view(PersistentColours())
            self.persistent_views_added = True

        print(f'Logged in as {self.user} (ID: {self.user.id})')


client = Client(case_insensitive=True, command_prefix=["o!","O!"], intents=Intents.all())

class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = Embed(color=Color.blurple(), description='')
        for page in self.paginator.pages:
            e.description += page
        e.set_footer(icon_url="https://cdn.discordapp.com/emojis/870161049633054752.png?size=96", text="Need help? Contact an admin or mod!")
        await destination.send(embed=e)

client.help_command = MyHelpCommand()
client.GOOGLE_API_KEY = GOOGLE_API_KEY
client.LOG_CHANNEL_ID = LOG_CHANNEL_ID

@client.command()
@commands.has_permissions(administrator=True)
async def verify(ctx):
    embed=Embed(title="Verify Here!", description="Click the button to verify!")
    await ctx.send(embed=embed, view=VerifyMenu())
    
    
@client.command()
@commands.has_any_role(822620759255154749, 935239717870518302)
async def prepare(ctx):
    """Starts a persistent view."""
    # In order for a persistent view to be listened to, it needs to be sent to an actual message.
    # Call this method once just to store it somewhere.
    # In a more complicated program you might fetch the message_id from a database for use later.
    # However this is outside of the scope of this simple example.
    await ctx.message.delete()
    await ctx.send("Choose your Colour Roles", view=PersistentColours())
    await ctx.send("Choose your Notification Roles", view=PersistentNotifs())
    await ctx.send("Choose your Giveaway Roles", view=PersistentGiveaways())


@client.event
async def on_command_error(message, error):
    if isinstance(error, CommandNotFound):
        await message.channel.send("Command Not Found.", delete_after=5)
    raise error


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.channel.id == 863302095603236884:
        await message.publish()
    #elif "http://" in message.content.lower() or "https://" in message.content.lower():
     #   if message.guild.get_role(913508354519883787) in message.author.roles or message.guild.get_role(822985879243980870) in message.author.roles or message.guild.get_role(9052e19932776710144) in message.author.roles or message.guild.get_role(903145807535030302) in message.author.roles or message.guild.get_role(862947013481594920) in message.author.roles:
      #      eee = ", ".join([y.name for y in message.author.roles])
       #     print(f"Bypassed link for {message.author} who has roles {eee}.\n\nSent this link: {message.content}")
        #    channel = message.guild.get_channel(LOG_CHANNEL_ID)
         #   embed = Embed(title="Bypassed link", description=f"{message.author} sent `{message.content}` in {message.channel}\n\nHas roles:\n`{eee}`", color=Color.green())
          #  await channel.send(embed=embed)
     #   else:
      #      print(f"Deleted Message from {message.author}.\n\nSent this link: {message.content}")
       #     await message.delete()
        #    channel = message.guild.get_channel(LOG_CHANNEL_ID)
         #   embed = Embed(title="Deleted link", description=f"{message.author} sent `{message.content}` in {message.channel}", color=Color.red())
          #  await channel.send(embed=embed)
    else:
        if message.content != "":
            if message.channel.id == 1076981668574941205: analyze_request = {'comment': { 'text': message.content }, 'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'IDENTITY_ATTACK': {}, 'INSULT': {}, 'PROFANITY': {}, 'THREAT': {}}}
            else:
                analyze_request = {
                  'comment': { 'text': message.content },
                  'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'IDENTITY_ATTACK': {}, 'INSULT': {}, 'PROFANITY': {}, 'THREAT': {}, 'SEXUALLY_EXPLICIT': {}, 'FLIRTATION': {}},
                  'languages': ["en"]
                }
            response = cclient.comments().analyze(body=analyze_request).execute()
            embed = Embed(title="High check", description=f"Comment Analyzer: {message.content}\n\n[Jump to message]({message.jump_url})")
            values = [embed.add_field(name=attribute.lower().title().replace("_", " "), value=str(100*round(Decimal(float(response['attributeScores'][attribute]['summaryScore']['value'])), 2)) + "%") for attribute in response['attributeScores'].keys()]

            toxscore = response['attributeScores']['TOXICITY']['summaryScore']['value']
            if response['attributeScores']['TOXICITY']['summaryScore']['value'] > 0.5:
                chan = client.get_channel(LOG_CHANNEL_ID)
                await chan.send(embed=embed.set_thumbnail(url=message.author.display_avatar))
                #await chan.send(embed=Embed(title="High toxicity", description=f"Toxicity score: {toxscore} out of 1.0\n\n{message.content}\n\n[Jump to message]({message.jump_url})").set_image(url=message.author.display_avatar))
            await client.process_commands(message)
#    else:
#        if message.attachments:
#            print(message.attachments[-1].url)
#            stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())
#
#            metadata = (('authorization', f'Key {CLARIFAI_API_KEY}'),)
#            request = service_pb2.PostModelOutputsRequest(
#                # model
#                model_id='e9576d86d2004ed1a38ba0cf39ecb4b1',
#                inputs=[
#                resources_pb2.Input(data=resources_pb2.Data(image=resources_pb2.Image(url=message.attachments[-1].url)))
#                ])
#            response = stub.PostModelOutputs(request, metadata=metadata)
#
#            if response.status.code != status_code_pb2.SUCCESS:
#                print("There was an error with your request!")
#                print("\tCode: {}".format(response.outputs[0].status.code))
#                print("\tDescription: {}".format(response.outputs[0].status.description))
#                print("\tDetails: {}".format(response.outputs[0].status.details))
#                raise Exception("Request failed, status code: " + str(response.status.code))
#            else:
#            #print(response.outputs[0].data.concepts)
#                for item in response.outputs[0].data.concepts:
#                    if 'nsfw' in item.name:
#                        n=item.value
#                print('%.2f' % (n))
#                if int('%.2f' % (n)) > int(0.5):
#                    for concept in response.outputs[0].data.concepts:
#                        q=str(concept.name)+str(": ")+str(concept.value)+str("\n")
#                        try:
#                            a=q+" "+o
#                        except UnboundLocalError:
#                            a=q
#                        try:
#                            o=a
#                        except UnboundLocalError:
#                            o=""
#                    await message.channel.send(o, delete_after=10)
#                    await message.delete()
#        else:
#            if message.content.startswith('!'):
#                pass
#            else:
#                roles=", ".join([str(r.name) for r in message.author.roles])
#                if "bypass" in roles:
#                    pass
#                else:
#                    metadata = (('authorization', f'Key {CLARIFAI_API_KEY}'),)
#                    userDataObject = resources_pb2.UserAppIDSet(user_id=str(os.environ['USR_ID']), app_id=str(os.environ['APP_ID']))
#
#                    channel = ClarifaiChannel.get_grpc_channel()
#                    stub = service_pb2_grpc.V2Stub(channel)
#                    post_model_outputs_response = stub.PostModelOutputs(
#                        service_pb2.PostModelOutputsRequest(
#                            user_app_id=userDataObject,
#                            model_id="c1a2ac2adba0204d859fb89fd44d6ac9",
#                            inputs=[
#                                resources_pb2.Input(
#                                    data=resources_pb2.Data(
#                                        text=resources_pb2.Text(
#                                            raw=str(message.content)
#                                        )
#                                    )
#                                )
#                            ]
#                        ),
#                        metadata=metadata
#                    )
#                    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
#                        print("There was an error with your request!")
#                        print("\tCode: {}".format(post_model_outputs_response.outputs[0].status.code))
#                        print("\tDescription: {}".format(post_model_outputs_response.outputs[0].status.description))
#                        print("\tDetails: {}".format(post_model_outputs_response.outputs[0].status.details))
#                        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)
#                    else:
#                        output = post_model_outputs_response.outputs[0]
#
#                        o=""
#                        for concept in output.data.concepts:
#                            value=round(Decimal(concept.value), 2)
#                            if int(value) > 0.50:
#                                q='yes-'+str(concept.name)+': '+str(value)
#                            else:
#                                q='no'
#                            try:
#                                a=q+" "+o
#                            except UnboundLocalError:
#                                a=q
#                            try:
#                                o=a
#                            except UnboundLocalError:
#                                o=""
#                        if "yes" in o:
#                            msg=o.replace('yes-', '').replace('no', '')
#                            content=message.content
#                            channel = client.get_channel(LOG_CHANNEL_ID)
#                            await channel.send(f"{message.author.name}#{message.author.discriminator} tried to cuss in {message.channel.name}.\n\nRatings/Predictions:\n{msg}\n\n{message.author.name} said `{content}`")
#                            await message.channel.send(msg, delete_after=10)
#                            await message.delete()
#        if message.channel.name == "destroyed":
#            print(str(message.author.name)+str(" said ")+str(message.content))
#            await client.process_commands(message)
#        else:
#            await client.process_commands(message)
        
client.load_extension("cogfunctions")
client.load_extension("Music")
client.load_extension("Moderation")
client.load_extension("Tasks")
client.load_extension("reactionroles")
client.run(TOKEN)
