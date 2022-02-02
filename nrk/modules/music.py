import typing as t

import hikari
from lavasnek_rs import NoSessionPresent
import lightbulb

music_plugin = lightbulb.Plugin('Music')


async def _join(ctx: lightbulb.Context) -> t.Optional[hikari.Snowflake]:
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


@music_plugin.command
@lightbulb.command(
    'connect', 'Connect to a voice channel'
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def connect(ctx: lightbulb.Context) -> None:
    channel_id = await _join(ctx)
    if channel_id:
        await ctx.respond(f"Joined <#{channel_id}>")


@music_plugin.command
@lightbulb.command(
    'disconnect', 'Disconnect from a voice channel'
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def disconnect(ctx: lightbulb.Context) -> None:
    await ctx.bot.lavalink.destroy(ctx.guild_id)
    await ctx.bot.update_voice_state(ctx.guild_id, None)
    await ctx.bot.lavalink.wait_for_connection_info_remove(ctx.guild_id)
    await ctx.bot.lavalink.remove_guild_node(ctx.guild_id)
    await ctx.bot.lavalink.remove_guild_from_loops(ctx.guild_id)
    await ctx.respond("Disconnected from voice channel.")


@music_plugin.command
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
        await _join(ctx)

    query_info = await ctx.bot.lavalink.auto_search_tracks(ctx.options.query)
    if not query_info.tracks:
        await ctx.respond("No tracks matching that query were found.")
        return

    try:
        await ctx.bot.lavalink.play(ctx.guild_id, query_info.tracks[0]).requester(ctx.author.id).queue()
        await ctx.respond(f"Added '{query_info.tracks[0].info.title}' to the queue.")
    except NoSessionPresent:
        await ctx.respond(f"No session found. Use /join to resolve this.")


@music_plugin.command
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


@music_plugin.command
@lightbulb.command(
    'queue', 'Displays the queue'
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def queue(ctx: lightbulb.Context) -> None:
    node = await ctx.bot.lavalink.get_guild_node(ctx.guild_id)
    if not node or not node.queue:
        await ctx.respond("There are no tracks in the queue.")
        return

    embed = (
        hikari.Embed(
            title="Queue",
            description=f"Showing {len(node.queue)} song(s).",
        )
            .add_field(name="Now playing", value=node.queue[0].track.info.title)
    )

    if len(node.queue) > 1:
        embed.add_field(name="Next up", value="\n".join(tq.track.info.title for tq in node.queue[1:]))

    await ctx.respond(embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(music_plugin)
