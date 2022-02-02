from . import music_plugin, lightbulb


@music_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command(
    'leave', 'Disconnect from a voice channel'
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def disconnect(ctx: lightbulb.Context) -> None:
    await ctx.bot.lavalink.destroy(ctx.guild_id)
    await ctx.bot.update_voice_state(ctx.guild_id, None)
    await ctx.bot.lavalink.wait_for_connection_info_remove(ctx.guild_id)
    await ctx.bot.lavalink.remove_guild_node(ctx.guild_id)
    await ctx.bot.lavalink.remove_guild_from_loops(ctx.guild_id)
    await ctx.respond("Disconnected from voice channel.")
