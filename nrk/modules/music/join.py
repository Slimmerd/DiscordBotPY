import lightbulb

from . import music_plugin, _join


@music_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command(
    'join', 'Connect to a voice channel'
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def connect(ctx: lightbulb.Context) -> None:
    channel_id = await _join.joint(ctx)
    if channel_id:
        await ctx.respond(f"Joined <#{channel_id}>")
