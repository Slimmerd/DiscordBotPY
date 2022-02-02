import hikari
import lightbulb

from . import music_plugin


@music_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command(
    'nowplaying', "Show's the song that is being played right now"
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def nowplaying(ctx: lightbulb.Context) -> None:
    node = await ctx.bot.lavalink.get_guild_node(ctx.guild_id)

    if not node or not node.queue:
        await ctx.respond("Nothing is being played at the moment")
        return

    em = hikari.Embed(
        title="Now playing",
        description=f"[{node.now_playing.track.info.title}]({node.now_playing.track.info.uri})",
    )

    await ctx.respond(embed=em)
