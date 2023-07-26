import twitchio
from twitchio.ext import commands, eventsub
import json

CFGf = open("config.realconfig", 'r')
CFG = json.load(CFGf)
CFGf.close()

bot = commands.Bot(token=CFG['oauth'], prefix="*=", initial_channels = ['poal48'])
es_cl = eventsub.EventSubClient(bot, CFG['cl_sc'], "http://localhost", CFG['api_token'])

@bot.command(name="sub")
async def sub(ctx):
    await es_cl.subscribe_channel_follows(276061388)
    await ctx.send("Subscribed!")

@bot.event()
async def eventsub_notification_follow(data):
    print(data)

bot.loop.create_task(es_cl.listen(port=4000))
bot.loop.create_task(bot.start())
bot.loop.run_forever()
