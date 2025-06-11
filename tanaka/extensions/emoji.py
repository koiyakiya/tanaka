import lightbulb
from lightbulb.exceptions import ExecutionPipelineFailedException
from lightbulb.prefab.cooldowns import fixed_window, OnCooldown
from lightbulb.prefab.checks import has_permissions
import hikari as h
import zipfile
from tanaka.utils.i18n import lcl
import io
from hikari.permissions import Permissions

loader = lightbulb.Loader()

group = lightbulb.Group('emoji', 'Emoji related commands')


@lightbulb.hook(lightbulb.ExecutionSteps.CHECKS)
async def is_owner_of_guild(
    _: lightbulb.ExecutionPipeline, ctx: lightbulb.Context
) -> None:
    if ctx.guild_id:
        guild = await ctx.client.rest.fetch_guild(ctx.guild_id)
        if ctx.user.id != guild.owner_id:
            raise Exception('yo')


@group.register
class EmojiClone(
    lightbulb.SlashCommand,
    name='cmds.emoji.clone.name',
    description='cmds.emoji.clone.description',
    hooks=[has_permissions(Permissions.MANAGE_GUILD_EXPRESSIONS)],
    localize=True,
):
    emoji = lightbulb.string(
        'cmds.emoji.clone.emoji.name',
        'cmds.emoji.clone.emoji.description',
        localize=True,
    )

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        if guild_id := ctx.guild_id:
            emoji: h.UnicodeEmoji | h.CustomEmoji = h.Emoji.parse(self.emoji)
            if isinstance(emoji, h.CustomEmoji):
                await ctx.client.rest.create_emoji(
                    guild_id, name=emoji.name, image=emoji
                )
                await ctx.respond(
                    lcl(ctx.interaction.locale, 'cmds.emoji.clone.success')
                )
            elif isinstance(emoji, h.UnicodeEmoji):
                emojis = await ctx.client.rest.fetch_application_emojis(
                    await ctx.client.rest.fetch_application()
                )
                embed = h.Embed()
                # TODO: I want to be able to get any application emoji (enum) at any time, maybe use dependency injection?
                for emoji in emojis:
                    if emoji.id == 1382165194058502164:
                        embed = h.Embed(
                            title=f'{emoji} error!',
                            description=lcl(
                                ctx.interaction.locale, 'cmds.emoji.clone.error'
                            ),
                        )
                await ctx.respond(embed=embed)


@group.register
class EmojiDownload(
    lightbulb.SlashCommand,
    name='download',
    description='Download all emojis from the guild.',
    hooks=[
        is_owner_of_guild,
        fixed_window(5.0, 1, 'global'),
    ],  # Limit the max number of interactions to only 1 per guild per 5 seconds in order to stop IO blocking
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.defer()  # Defer since IO may block shit if spammed
        if guild_id := ctx.guild_id:
            # Get all emojis currently in the guild
            if emojis := await ctx.client.rest.fetch_guild_emojis(guild_id):
                buffer = io.BytesIO()  # Write the zip file into memory
                with zipfile.ZipFile(buffer, 'w') as img_zip:
                    for emoji in emojis:
                        img_zip.writestr(
                            f'{emoji.name}_{emoji.id}.{emoji.extension.split("/")[0] if emoji.extension else ""}',
                            await emoji.read(),
                        )
                buffer.seek(0)  # Change stream position back to 0
                await ctx.respond(attachment=h.Bytes(buffer.getvalue(), 'emojis.zip'))


@group.register
class EmojiPurge(
    lightbulb.SlashCommand,
    name='purge',
    description='Purge all custom emojis from this guild.',
    hooks=[is_owner_of_guild],
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.defer()  # deferring since rest API shit might take a while
        if guild_id := ctx.guild_id:
            if emojis := await ctx.client.rest.fetch_guild_emojis(guild_id):
                for emoji in emojis:
                    await ctx.client.rest.delete_emoji(guild_id, emoji)
                await ctx.respond('Successfully deleted all emojis.')
            else:
                await ctx.respond('No emojis to delete.')


@loader.error_handler
async def emoji_error_handler(exc: ExecutionPipelineFailedException) -> bool:
    for exception in exc.causes:  # A bit weird and different compared to arc but
        if isinstance(exception, OnCooldown):
            await exc.context.respond('This command is currently on cooldown!')
            return True
    return True


loader.command(group)
