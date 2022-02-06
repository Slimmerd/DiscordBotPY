import datetime

import hikari
import lightbulb

from . import moderation_plugin


@moderation_plugin.command
@lightbulb.option(
    'user', 'Mention the user you want to kick',
)
@lightbulb.option(
    'reason', 'Why do you want to kick this user?',
)
@lightbulb.command(
    "kick", "Kicks a tagged member"
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def kick(ctx: lightbulb.Context) -> None:
    [user, reason] = ctx.options
    guild = ctx.get_guild()

    await guild.kick(user=user, reason=reason)

    embed = (
        hikari.Embed(
            title=f'⛔️ **{user}** kicked',
            color='#13be43',
            timestamp=datetime.datetime.now(),
        )
            .set_author(
            name=guild.name,
            icon=guild.icon_url
        )
            .set_thumbnail(
            guild.icon_url
        )
            .set_footer(
            icon=ctx.author.avatar_url,
            text=ctx.author.username
        )
    )

    await ctx.respond(embed)
