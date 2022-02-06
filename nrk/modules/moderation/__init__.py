import lightbulb

from ._load import moderation_plugin
from .ban import ban
from .kick import kick
# from .mute import mute
# from .unmute import unmute
# from .warn import warn
# from .infractions import infractions
# from .clear_infractions import clear_infractions


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(moderation_plugin)
