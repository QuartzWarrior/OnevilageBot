from nextcord.ext import tasks, commands
#import subprocess, os

class Tasks(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.updates.start()

    def cog_unload(self):
        self.updates.cancel()

    @tasks.loop(hours=5.0)
    async def updates(self):
        #print("Starting background updates...\n")
        #process=subprocess.Popen(["python","-m","pip","install","-U","-r","requirements.txt"])
        #process.communicate()
        #os.system("clear")
        #print("\nBackground updates finished.")
        pass

    @updates.before_loop
    async def before_updates(self):
        await self.client.wait_until_ready()
def setup(client):
    client.add_cog(Tasks(client))
