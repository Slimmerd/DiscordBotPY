from __future__ import annotations

import time
from datetime import timedelta
from platform import python_version
import typing as t

import hikari
import lightbulb
from psutil import Process, virtual_memory

from . import meta_plugin


@meta_plugin.command
@lightbulb.command(
    "stats", "Display stats about the bot"
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def stats(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    proc = Process()

    with proc.oneshot():
        uptime = timedelta(seconds=time.time() - proc.create_time())
        cpu_time = str(timedelta(seconds=(cpu := proc.cpu_times()).system + cpu.user))
        mem_total = virtual_memory().total / (1024 ** 2)
        mem_of_total = proc.memory_percent()
        mem_usage = mem_total * (mem_of_total / 100)

    fields: t.Optional[list[tuple[str | int, str | int, bool]]] = [
        ("OttBot", f"```{ctx.bot.__version__}```", True),
        ("Python", f"```{python_version()}```", True),
        ("Hikari", f"```{hikari.__version__}```", True),
        (
            "Users here",
            f"```{len([_ async for _ in guild.fetch_members(ctx.guild_id)] if ctx.guild_id else [])}```",
            True,
        ),
        ("Total users", f"```{len(ctx.bot.cache.get_users_view()):,}```", True),
        ("Servers", f"```{ctx.bot.shard_count:,}```", True),
        ("Latency", f"```{ctx.bot.heartbeat_latency * 1000:,.0f} ms```", True),
        (
            "Memory usage",
            f"```| {mem_of_total:>5,.2f}% | {mem_usage:,.0f} MiB  /  {(mem_total):,.0f} MiB |```",
            False,
        ),
        ("Uptime", f"```{str(uptime)[:-4]}```", True),
        ("CPU time", f"```{cpu_time[:-4]}```", True),
    ]

    me = ctx.bot.get_me()

    embed = (
        hikari.Embed(
            title="System stats",
            color=me.get_me().accent_color
        )
        .set_thumbnail(me.avatar_url)

    )

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    await ctx.respond(
        embed=embed
        ),
