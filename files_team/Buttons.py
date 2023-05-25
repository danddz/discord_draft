
from discord.ext import commands, tasks
from discord.ui import Button, View
import discord

import files_team.name_buttons as name_buttons

class TeamButton(Button):
    def __init__(self, label, msg, count_players, max_count_players, creator_id):
        style = discord.ButtonStyle.green
        if label == name_buttons.list_1[1]:
            style = discord.ButtonStyle.red
        elif label == name_buttons.list_1[2]:
            style = discord.ButtonStyle.blurple

        super().__init__(label=label, style=style)

        self.label = label
        self.msg = msg
        self.count_players = count_players
        self.max_count_players = max_count_players
        self.creator_id = creator_id

    async def callback(self, interaction):
        flag = 0
        interaction_user_id = '<@' + str(interaction.user.id) + '>'

        if self.label in name_buttons.list_0:
            self.max_count_players = int(self.label)
            tmp = '' if 'Играют:' in self.msg else 'Играют:'
            self.msg = self.msg.replace(', выберите количество человек.', f', набирает команду из {self.label} человек. {tmp}')
            flag = 1
        elif self.label == name_buttons.list_1[0]:
            if interaction_user_id not in self.msg:
                self.msg += '\n' + interaction_user_id
                self.count_players += 1
                flag = 1
        elif self.label == name_buttons.list_1[1]:
            if interaction_user_id in self.msg[1:]:
                self.msg = self.msg.replace('\n' + interaction_user_id, '')
                self.count_players -= 1
                flag = 1
        elif self.label == name_buttons.list_1[2] and self.creator_id == interaction_user_id:
            flag = 2

        if flag == 1 or flag == 2:
            view = View(timeout=60*60)

            if self.count_players < self.max_count_players and flag != 2:
                for i in name_buttons.list_1:
                    view.add_item(TeamButton(i, self.msg, self.count_players, self.max_count_players, self.creator_id))

            await interaction.response.edit_message(content=self.msg, view=view)
        else:
            await interaction.response.defer()
