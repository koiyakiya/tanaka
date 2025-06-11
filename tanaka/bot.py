from __future__ import annotations

__all__ = ('bot',)

from hikari import Intents
import hikari
import lightbulb
from tanaka.config import __TOKEN__
import tanaka.extensions as extensions
from tanaka.utils.i18n import _lcldict

bot = hikari.GatewayBot(
    token=__TOKEN__,
    intents=(
        Intents.GUILDS
        | Intents.GUILD_MESSAGES
        | Intents.GUILD_MESSAGE_REACTIONS
        | Intents.GUILD_INVITES
        | Intents.DM_MESSAGES
        | Intents.GUILD_MESSAGE_POLLS
    ),
)
client = lightbulb.client_from_app(bot, localization_provider=_lcldict)


@bot.listen(hikari.StartingEvent)
async def on_starting(_: hikari.StartingEvent) -> None:
    await client.load_extensions_from_package(extensions)
    await client.start()


@client.register()
class Ping(lightbulb.SlashCommand, name='ping', description='checks the bot is alive'):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.respond('Pong!')
