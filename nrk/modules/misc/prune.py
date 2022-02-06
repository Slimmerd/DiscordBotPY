import datetime

import hikari
import lightbulb

from . import misc_plugin


@misc_plugin.command
@lightbulb.option(
    "amount", "Number of messages to delete", default=None, min=1, max=100
)
@lightbulb.command(
    "prune", "Deletes messages in the chat"
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def prune(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    channel = ctx.get_channel()
    messages = []

    async for message in channel.fetch_history():
        if len(messages) >= ctx.options.x:
            break
        messages += [message]

    await channel.delete_messages(messages)

    embed = (
        hikari.Embed(
            color='red',
            timestamp=datetime.datetime.now().astimezone(),
            title=f"Messages deleted",
            description=f'{len(messages)}'
        )
            .set_thumbnail(guild.avatar_url)
            .set_footer(text=f"Requested by {ctx.author}", icon=ctx.author.avatar_url)
    )

    await ctx.respond(embed=embed)
