import datetime

import hikari
import lightbulb

from . import meta_plugin


@meta_plugin.command
@lightbulb.option(
    "user", "The user to get information about", default=None
)
@lightbulb.command(
    "user_info", "Information about a user"
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def user_info(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    member: hikari.Member = ctx.options.member or ctx.member

    created_at = int(member.created_at.timestamp())
    joined_at = int(member.joined_at.timestamp())

    roles = (await member.fetch_roles())[1:]

    perms = hikari.Permissions.NONE

    for role in roles:
        perms |= role.permissions

    permissions = str(perms).split("|")

    status = (
        member.get_presence().visible_status if member.get_presence() else "Offline"
    )

    if member.id == guild.owner_id:
        acknowlegdement = "Server Owner"
    elif "ADMINISTRATOR" in permissions:
        acknowlegdement = "Administrator"
    elif "MANAGE_GUILD" in permissions:
        acknowlegdement = "Moderator"
    elif "MANAGE_MESSAGES" in permissions:
        acknowlegdement = "Staff"
    else:
        acknowlegdement = "Member"

    embed = (
        hikari.Embed(
            color='red',
            timestamp=datetime.datetime.now().astimezone(),
            title=f"Userinfo of {member}",
        )
            .set_thumbnail(member.avatar_url)
            .set_footer(text=f"Requested by {ctx.author}", icon=ctx.author.avatar_url)
    )

    fields = [
        ("ID", member.id, True),
        ("Joined", f"<t:{joined_at}:F> • <t:{joined_at}:R>", True),
        ("Created", f"<t:{created_at}:F> • <t:{created_at}:R>", True),
        ("Status", status.title(), True),
        ("Acknowledgement", acknowlegdement, True),
        ("Is Bot", member.is_bot, True),
        (
            "Permissions",
            ", ".join(perm.replace("_", " ").title() for perm in permissions),
            False,
        ),
        ("Roles", ", ".join(r.mention for r in roles) if roles else "@everyone", False),
    ]

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    await ctx.respond(embed=embed)
