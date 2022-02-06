import datetime

import hikari
import lightbulb

from . import meta_plugin


@meta_plugin.command
@lightbulb.option(
    "target", "The member to get information about.", hikari.User, required=False
)
@lightbulb.command(
    "server_info", "Information about the current server information"
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def server_info(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    members_mapping = guild.get_members()
    members = [member for member in members_mapping.values() if not member.is_bot]
    bots = [member for member in members_mapping.values() if member.is_bot]
    created_at = int(guild.created_at.timestamp())
    roles = guild.get_roles()
    embed = (
        hikari.Embed(color='green', timestamp=datetime.datetime.now().astimezone())
            .set_thumbnail(guild.icon_url)
            .set_footer(text=f"Requested by {ctx.author}", icon=ctx.author.avatar_url)
    )
    fields = [
        ("ID", guild.id, True),
        ("Owner", f"<@{guild.owner_id}>", True),
        ("Members", len(members), True),
        ("Bots", len(bots), True),
        ("Created", f"<t:{created_at}:F> • <t:{created_at}:R>", True),
        ("Channel Count", len(guild.get_channels()), True),
        ("Boost Count", guild.premium_subscription_count, True),
        ("Premium Tier", str(guild.premium_tier).replace("_", " ").title(), True),
        ("Role Count", len(guild.get_roles()), True),
        (
            "Vanity URL",
            f"https://discord.gg/{guild.vanity_url_code}"
            if guild.vanity_url_code
            else "None",
            True,
        ),
        (
            "Roles",
            ", ".join(r.mention for r in roles.values() if not r.name == "@everyone"),
            False,
        ),
    ]

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    if guild.features:
        embed.add_field(
            name="Guild Features",
            value="\n".join(
                "• " + feature.replace("_", " ").title() for feature in guild.features
            ),
            inline=False,
        )

    await ctx.respond(embed=embed)
