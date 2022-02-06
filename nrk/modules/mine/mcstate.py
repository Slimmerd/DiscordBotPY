import os

import lightbulb
from dotenv import load_dotenv

from . import mine_plugin
from mcipc.query import Client

load_dotenv()

@mine_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command(
    'mcstate', 'Shows minecraft server state'
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def mcstate(ctx: lightbulb.Context) -> None:
    try:
        with Client(os.getenv("MINECRAFT_HOST"), int(os.getenv("MINECRAFT_PORT")), timeout=1.5) as client:
            basic_stats = client.basic_stats
            await ctx.respond(
                basic_stats.motd + ' is online! With ' + str(basic_stats.num_players) + ' out of ' + str(
                    basic_stats.max_players) + ' players.')

    except:
        await ctx.respond('Server is offline!')
