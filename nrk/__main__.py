import os

from nrk.init import Bot

if os.name != "nt":
    import uvloop

    uvloop.install()

if __name__ == "__main__":
    bot = Bot()
    bot.run()
