import lightbulb

from ._load import misc_plugin
from .prune import prune


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(misc_plugin)
