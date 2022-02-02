import lightbulb

from . import music_plugin
from nrk.utils.Equalizers import Equalizers


@music_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option('filter_name', 'Select EQ filter name', choices=("flat", "boost", "metal", "piano"))
@lightbulb.command(
    'eq', "Add a filter to the current song"
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def eq(ctx: lightbulb.Context) -> None:
    node = await ctx.bot.lavalink.get_guild_node(ctx.guild_id)
    filter_name = ctx.options.filter_name

    if not node or not node.queue:
        await ctx.respond("No song playing right now")
        return

    if filter_name == "flat":
        await ctx.bot.lavalink.equalize_all(ctx.guild_id, Equalizers().flat())
        await ctx.respond(f"Applied the filter `{filter_name}` successfully")
    elif filter_name == "boost":
        await ctx.bot.lavalink.equalize_all(ctx.guild_id, Equalizers().boost())
        await ctx.respond(f"Applied the filter `{filter_name}` successfully")
    elif filter_name == "metal":
        await ctx.bot.lavalink.equalize_all(ctx.guild_id, Equalizers().metal())
        await ctx.respond(f"Applied the filter `{filter_name}` successfully")
    elif filter_name == "piano":
        await ctx.bot.lavalink.equalize_all(ctx.guild_id, Equalizers().piano())
        await ctx.respond(f"Applied the filter `{filter_name}` successfully")
    else:
        pass
