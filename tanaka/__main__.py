import asyncio
import os

from tanaka.bot import bot

if __name__ == '__main__':
    if os.name != 'nt':
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    bot.run()
