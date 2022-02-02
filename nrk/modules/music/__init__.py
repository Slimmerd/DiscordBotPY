import lightbulb

from ._load import music_plugin
from .skip import skip
from .play import play
from .pause import pause
from .resume import resume
from .queue import queue
from .join import connect
from .leave import disconnect
from .volume import volume
from .eq import eq
from .now_playing import nowplaying


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(music_plugin)
