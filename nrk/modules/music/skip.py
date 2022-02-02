import lightbulb

from . import music_plugin


@music_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command(
    'skip', 'Skips a song in the queue'
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def skip(ctx: lightbulb.Context) -> None:
    _skip = await ctx.bot.lavalink.skip(ctx.guild_id)
    node = await ctx.bot.lavalink.get_guild_node(ctx.guild_id)

    if not _skip:
        await ctx.respond("Nothing to skip.")
        return

    if not node.queue and not node.now_playing:
        await ctx.bot.lavalink.stop(ctx.guild_id)

    await ctx.respond(f"Skipped '{_skip.track.info.title}'")
