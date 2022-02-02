import hikari
import lightbulb
import typing as t


async def joint(ctx: lightbulb.Context) -> t.Optional[hikari.Snowflake]:
    states = ctx.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]

    if not voice_state:
        await ctx.respond("Not connected to a voice channel.")
        return None

    channel_id = voice_state[0].channel_id

    await ctx.bot.update_voice_state(ctx.guild_id, channel_id, self_deaf=True)
    connection_info = await ctx.bot.lavalink.wait_for_full_connection_info_insert(ctx.guild_id)

    await ctx.bot.lavalink.create_session(connection_info)
    return channel_id
