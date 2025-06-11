import lightbulb
import hikari

loader = lightbulb.Loader()


@loader.listener(hikari.MessageCreateEvent)
async def on_message(msg: hikari.MessageCreateEvent) -> None:
    """A secret command only usable by the bot owner to manage application emojis easily."""
    if msg.content:
        if msg.author_id == 1230675687967555635:
            command = msg.content.split()
            if len(command) == 2:
                if command[0].startswith('?emoji') and command:
                    emoji = hikari.Emoji.parse(command[1])
                    if isinstance(emoji, hikari.CustomEmoji):
                        fetched_emoji = await msg.app.rest.create_application_emoji(
                            await msg.app.rest.fetch_application(),
                            name=emoji.name,
                            image=await emoji.read(),
                        )
                        await msg.message.respond(
                            f'{fetched_emoji.mention} Emoji has been added to the application.'
                        )
                if command[0].startswith('?emojipurge') and command:
                    if command[1] == 'confirm':
                        emojis = await msg.app.rest.fetch_application_emojis(
                            await msg.app.rest.fetch_application()
                        )
                        if emojis:
                            for emoji in emojis:
                                await msg.app.rest.delete_application_emoji(
                                    await msg.app.rest.fetch_application(), emoji
                                )
                            await msg.message.respond(
                                'All emojis have been purged from the application.'
                            )
