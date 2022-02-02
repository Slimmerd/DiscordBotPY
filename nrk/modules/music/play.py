import lightbulb
from lavasnek_rs import NoSessionPresent

from . import music_plugin, _join


@music_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option(
    'query', 'The track to play'
)
@lightbulb.command(
    'play', 'Play a track'
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def play(ctx: lightbulb.Context) -> None:
    cxn = await ctx.bot.lavalink.get_guild_gateway_connection_info(ctx.guild_id)
    if not cxn:
        await _join.joint(ctx)

    query_info = await ctx.bot.lavalink.auto_search_tracks(ctx.options.query)
    if not query_info.tracks:
        await ctx.respond("No tracks matching that query were found.")
        return

    try:
        await ctx.bot.lavalink.play(ctx.guild_id, query_info.tracks[0]).requester(ctx.author.id).queue()
        await ctx.respond(f"Added '{query_info.tracks[0].info.title}' to the queue.")
    except NoSessionPresent:
        await ctx.respond(f"No session found. Use /join to resolve this.")
