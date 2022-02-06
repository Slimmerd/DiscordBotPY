import hikari
import lightbulb

from . import music_plugin


@music_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
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
        ).add_field(name="Now playing", value=node.queue[0].track.info.title)
    )

    if len(node.queue) > 1:
        embed.add_field(name="Next up", value="\n".join(tq.track.info.title for tq in node.queue[1:]))

    await ctx.respond(embed)
