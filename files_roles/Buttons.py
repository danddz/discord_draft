from discord.ext import commands, tasks
from discord.ui import Button, View
import discord
import random
import requests

class RolesButton(Button):
    def __init__(self, label, msg, roles_buttons_dict):
        style = discord.ButtonStyle.grey
        super().__init__(label=label, style=style, emoji=roles_buttons_dict[label][1])
        self.label = label
        self.msg = msg
        self.roles_buttons_dict = roles_buttons_dict

    async def callback(self, interaction):
        role = -1
        view = View(timeout=60*60)

        if self.label in self.roles_buttons_dict.keys():
            id_ = self.roles_buttons_dict[self.label][0]
            role = interaction.guild.get_role(id_)

        if role != -1 and role not in interaction.user.roles:
            await interaction.user.add_roles(role)
        else:
            await interaction.user.remove_roles(role)

        await interaction.response.defer()
