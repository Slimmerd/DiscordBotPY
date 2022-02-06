import hikari
import lightbulb

moderation_plugin = lightbulb.Plugin('Moderation')
moderation_plugin.add_checks(
    lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_GUILD)
)
