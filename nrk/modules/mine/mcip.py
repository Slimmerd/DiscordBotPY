import os

import lightbulb
from dotenv import load_dotenv
from . import mine_plugin

load_dotenv()


@mine_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command(
    'mcip', 'Shows minecraft server IP'
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def mcip(ctx: lightbulb.Context) -> None:
    await ctx.respond('The IP is `' + os.getenv("MINECRAFT_HOST") + '`')
