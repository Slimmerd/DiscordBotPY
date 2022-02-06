import lightbulb

from ._load import mine_plugin
from .mcip import mcip
from .mclist import mclist
from .mcstate import mcstate

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(mine_plugin)
