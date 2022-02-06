import hikari
import lightbulb

misc_plugin = lightbulb.Plugin('Misc')
misc_plugin.add_checks(
    lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_GUILD)
)
