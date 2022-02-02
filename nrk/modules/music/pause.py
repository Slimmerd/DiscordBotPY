import lightbulb

from . import music_plugin


@music_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command(
    'pause', "Pause the current song being played"
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def pause(ctx: lightbulb.Context) -> None:
    node = await ctx.bot.lavalink.get_guild_node(ctx.guild_id)

    if not node or not node.queue:
        await ctx.respond("Nothing is being played at the moment")
        return

    if node.is_paused:
        await ctx.respond("The songs are currently paused")
        return

    await ctx.bot.lavalink.pause(ctx.guild_id)
    await ctx.bot.lavalink.set_pause(ctx.guild_id, True)
    await ctx.respond("Paused successfully")

