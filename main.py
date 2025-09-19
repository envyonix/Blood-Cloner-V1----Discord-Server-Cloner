import os
import discord
import asyncio
from colorama import Fore, Style, init
from serverclone import Clone


init(autoreset=True)


try:
    os.system("cls" if os.name == "nt" else "clear")
except Exception:
    pass


print(f"""{Fore.RED}

 ______   _        _______  _______  ______  
(  ___ \ ( \      (  ___  )(  ___  )(  __  \ 
| (   ) )| (      | (   ) || (   ) || (  \  )
| (__/ / | |      | |   | || |   | || |   ) |
|  __ (  | |      | |   | || |   | || |   | |
| (  \ \ | |      | |   | || |   | || |   ) |
| )___) )| (____/\| (___) || (___) || (__/  )
|/ \___/ (_______/(_______)(_______)(______/  

{Style.RESET_ALL}
                                                            {Fore.MAGENTA}Blood Copier V1-By Envyonix{Style.RESET_ALL}
        """)

# Inputs
token = input(f'Please enter your bot token:\n > ').strip()
guild_s = input('Please enter guild ID you want to copy FROM:\n > ').strip()
guild = input('Please enter guild ID you want to copy TO:\n > ').strip()

print("\n\n")

# Discord client setup
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as: {Fore.GREEN}{client.user}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Cloning Server...{Style.RESET_ALL}")

    guild_from = client.get_guild(int(guild_s))
    guild_to = client.get_guild(int(guild))

    if not guild_from or not guild_to:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Could not find one or both guilds. Check the IDs and bot permissions.")
        await client.close()
        return

    # Steps
    await Clone.guild_edit(guild_to, guild_from)
    await Clone.roles_delete(guild_to)
    await Clone.channels_delete(guild_to)
    await Clone.roles_create(guild_to, guild_from)
    await Clone.categories_create(guild_to, guild_from)
    await Clone.channels_create(guild_to, guild_from)
    await Clone.emojis_delete(guild_to)
    await Clone.emojis_create(guild_to, guild_from)

    print(f"""{Fore.GREEN}

 ______   _        _______  _______  ______  
(  ___ \ ( \      (  ___  )(  ___  )(  __  \ 
| (   ) )| (      | (   ) || (   ) || (  \  )
| (__/ / | |      | |   | || |   | || |   ) |
|  __ (  | |      | |   | || |   | || |   | |
| (  \ \ | |      | |   | || |   | || |   ) |
| )___) )| (____/\| (___) || (___) || (__/  )
|/ \___/ (_______/(_______)(_______)(______/  

    {Style.RESET_ALL}""")

    await asyncio.sleep(5)
    await client.close()

client.run(token)
