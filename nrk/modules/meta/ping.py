import time

import lightbulb

from . import meta_plugin


@meta_plugin.command
@lightbulb.command(
    "ping", "Ping the bot to check if it's online"
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    before = time.time()
    msg = await ctx.respond("Pong!", ensure_result=True)
    after = time.time()

    await msg.edit(
        f"{msg.message}\n**Gateway**: {ctx.bot.heartbeat_latency * 1000:,.0f} ms\n**REST**: {(after - before) * 1000:,.0f} ms",
    )
