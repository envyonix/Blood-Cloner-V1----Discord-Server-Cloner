import discord
from colorama import Fore, Style

def print_add(message): print(f'{Fore.GREEN}[+]{Style.RESET_ALL} {message}')
def print_delete(message): print(f'{Fore.RED}[-]{Style.RESET_ALL} {message}')
def print_warning(message): print(f'{Fore.YELLOW}[WARNING]{Style.RESET_ALL} {message}')
def print_error(message): print(f'{Fore.RED}[ERROR]{Style.RESET_ALL} {message}')

class Clone:
    @staticmethod
    async def roles_delete(guild_to: discord.Guild):
        for role in guild_to.roles:
            if role.name != "@everyone":
                try:
                    await role.delete()
                    print_delete(f"Deleted Role: {role.name}")
                except Exception as e:
                    print_error(f"Failed to delete role {role.name}: {e}")

    @staticmethod
    async def roles_create(guild_to: discord.Guild, guild_from: discord.Guild):
        roles = [r for r in guild_from.roles if r.name != "@everyone"][::-1]
        for role in roles:
            try:
                await guild_to.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    colour=role.colour,
                    hoist=role.hoist,
                    mentionable=role.mentionable
                )
                print_add(f"Created Role: {role.name}")
            except Exception as e:
                print_error(f"Failed to create role {role.name}: {e}")

    @staticmethod
    async def channels_delete(guild_to: discord.Guild):
        for channel in guild_to.channels:
            try:
                await channel.delete()
                print_delete(f"Deleted Channel: {channel.name}")
            except Exception as e:
                print_error(f"Failed to delete channel {channel.name}: {e}")

    @staticmethod
    async def categories_create(guild_to: discord.Guild, guild_from: discord.Guild):
        for channel in guild_from.categories:
            try:
                overwrites_to = {
                    discord.utils.get(guild_to.roles, name=key.name): value
                    for key, value in channel.overwrites.items()
                    if discord.utils.get(guild_to.roles, name=key.name)
                }
                new_cat = await guild_to.create_category(name=channel.name, overwrites=overwrites_to)
                await new_cat.edit(position=channel.position)
                print_add(f"Created Category: {channel.name}")
            except Exception as e:
                print_error(f"Failed to create category {channel.name}: {e}")

    @staticmethod
    async def channels_create(guild_to: discord.Guild, guild_from: discord.Guild):
        for ch in guild_from.text_channels + guild_from.voice_channels:
            try:
                category = None
                if ch.category:
                    category = discord.utils.get(guild_to.categories, name=ch.category.name)

                overwrites_to = {
                    discord.utils.get(guild_to.roles, name=key.name): value
                    for key, value in ch.overwrites.items()
                    if discord.utils.get(guild_to.roles, name=key.name)
                }

                if isinstance(ch, discord.TextChannel):
                    new_ch = await guild_to.create_text_channel(
                        name=ch.name,
                        overwrites=overwrites_to,
                        position=ch.position,
                        topic=getattr(ch, "topic", None),
                        slowmode_delay=getattr(ch, "slowmode_delay", 0),
                        nsfw=getattr(ch, "nsfw", False)
                    )
                else:
                    new_ch = await guild_to.create_voice_channel(
                        name=ch.name,
                        overwrites=overwrites_to,
                        position=ch.position,
                        bitrate=getattr(ch, "bitrate", None),
                        user_limit=getattr(ch, "user_limit", None)
                    )

                if category:
                    await new_ch.edit(category=category)
                print_add(f"Created Channel: {ch.name}")
            except Exception as e:
                print_error(f"Failed to create channel {ch.name}: {e}")

    @staticmethod
    async def emojis_delete(guild_to: discord.Guild):
        for emoji in guild_to.emojis:
            try:
                await emoji.delete()
                print_delete(f"Deleted Emoji: {emoji.name}")
            except Exception as e:
                print_error(f"Failed to delete emoji {emoji.name}: {e}")

    @staticmethod
    async def emojis_create(guild_to: discord.Guild, guild_from: discord.Guild):
        for emoji in guild_from.emojis:
            try:
                emoji_image = await emoji.read()
                await guild_to.create_custom_emoji(name=emoji.name, image=emoji_image)
                print_add(f"Created Emoji: {emoji.name}")
            except Exception as e:
                print_error(f"Failed to create emoji {emoji.name}: {e}")

    @staticmethod
    async def guild_edit(guild_to: discord.Guild, guild_from: discord.Guild):
        try:
            icon_image = None
            if guild_from.icon:
                try:
                    icon_image = await guild_from.icon.read()
                except Exception:
                    print_warning(f"Could not read icon from {guild_from.name}")

            await guild_to.edit(name=guild_from.name)
            if icon_image:
                await guild_to.edit(icon=icon_image)
                print_add(f"Guild icon updated: {guild_to.name}")
        except Exception as e:
            print_error(f"Failed to edit guild {guild_to.name}: {e}")
