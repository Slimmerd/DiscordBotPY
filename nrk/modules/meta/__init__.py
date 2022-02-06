import lightbulb

from ._load import meta_plugin
from .server_info import server_info
from .ping import ping
from .user_info import user_info
from .stats import stats


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(meta_plugin)
