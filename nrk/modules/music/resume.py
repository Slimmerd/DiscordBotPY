import lightbulb

from . import music_plugin


@music_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command(
    'resume', "Resume the song that is paused"
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def resume(ctx: lightbulb.Context) -> None:
    node = await ctx.bot.lavalink.get_guild_node(ctx.guild_id)

    if not node or not node.queue:
        await ctx.respond("Nothing is being played at the moment")
        return

    if node.is_paused:
        await ctx.bot.lavalink.resume(ctx.guild_id)
        await ctx.respond("Resumed successfully")
    else:
        await ctx.respond("It's already resumed >:(")
