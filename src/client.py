from typing import cast

import discord
from discord.ext import commands

import db, snowballs
from config import SNOWBALL_LOG

class DiscordClient(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="?", intents=intents)

    async def set_data(self, _: discord.Guild):
        self.log = cast(discord.TextChannel, self.get_channel(SNOWBALL_LOG))

    async def sync_guild(self, guild: discord.Guild):
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

client = DiscordClient()

@client.tree.command(name="snowballs", description="List how many snowballs you have remaining")
async def showball_count_slash(interaction: discord.Interaction):
    cnt = db.get_snowballs(interaction.user.id)
    await interaction.response.send_message(f"You have {cnt} snowball(s) remaining", ephemeral=True)

@client.tree.command(name="leaderboard", description="Post the leaderboard")
async def post_leaderboard_content(interaction: discord.Interaction):
    leaders = db.get_leaders()
    output = "__**Top 10 Most Hit Users**__"
    for leader in leaders:
        output += f"\n{leader[1]} **-** <@{leader[0]}>"
    await interaction.response.send_message(output)

@client.tree.context_menu(name="Throw snowball")
async def throw_snowball_msg_context(interaction: discord.Interaction, message: discord.Message):
    if interaction.user != message.author:
        output = snowballs.throw_snowball(interaction.user, message.author)
        await client.log.send(output)
        await message.add_reaction("⚪")
        await interaction.response.send_message(output, ephemeral=True)
    else:
        await interaction.response.send_message("You can't throw a snowball at yourself!", ephemeral=True)
