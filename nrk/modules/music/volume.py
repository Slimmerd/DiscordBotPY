import lightbulb

from . import music_plugin


@music_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option(
    'volume', 'Volume to be set (Between 0 and 100)', type=float, min_value=0, max_value=100
)
@lightbulb.command(
    'volume', 'Increase/Decrease the volume'
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def volume(ctx: lightbulb.Context) -> None:
    node = await ctx.bot.lavalink.get_guild_node(ctx.guild_id)
    _volume = ctx.options.volume

    if not node or not node.now_playing:
        await ctx.respond("Nothing is being played at the moment")
        return

    if 0 < _volume < 100:
        await ctx.bot.lavalink.volume(ctx.guild_id, _volume)
        await ctx.respond(f"Set the volume to {_volume}")
    else:
        await ctx.respond("Volume should be between 0 and 100")
