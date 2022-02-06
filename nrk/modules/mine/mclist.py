import os

import lightbulb
from dotenv import load_dotenv
from . import mine_plugin
from mcipc.query import Client

load_dotenv()


@mine_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command(
    'mclist', 'Shows players list'
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def mclist(ctx: lightbulb.Context) -> None:
    try:
        with Client(os.getenv("MINECRAFT_HOST"), int(os.getenv("MINECRAFT_PORT")), timeout=1.5) as client:
            full_stats = client.full_stats
            player_list_message = "Player list: \n"
            for player_name in full_stats.players:
                player_list_message = player_list_message + "- " + player_name + "\n"

            await ctx.respond(player_list_message)

    except:
        await ctx.respond('Server is offline!')
