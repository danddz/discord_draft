from discord.ext import commands, tasks
from discord.ui import Button, View
import discord
import files_pvp.pvp_settings as pvp_settings
import files_pvp.Pokemons_PvP as Pokemons_PvP
import random
import time
import os

class PvPButton(Button):
    def __init__(self, label, msg, flag, users, users_nicks, teams, order, index):
        style = discord.ButtonStyle.green
        if label in teams[flag]:
            style = discord.ButtonStyle.red
        elif label == '<-' or label == '->':
            style = discord.ButtonStyle.blurple

        super().__init__(label=label, style=style)
        self.label = label
        self.msg = msg
        self.flag = flag
        self.users = users
        self.users_nicks = users_nicks
        self.teams = teams
        self.order = order
        self.index = index

    async def callback(self, interaction):
        view = View(timeout=60*60)
        msg_flag = 0
        if str(interaction.user.id) in self.users[self.flag]:
            if str(interaction.user)[:-5] not in self.users_nicks:
                self.users_nicks.append(str(interaction.user)[:-5])

            if self.label == '->':
                for i in Pokemons_PvP.list_2:
                    view.add_item(PvPButton(i, self.msg, self.flag, self.users, self.users_nicks, self.teams, self.order, self.index))
            elif self.label == '<-':
                for i in Pokemons_PvP.list_1:
                    view.add_item(PvPButton(i, self.msg, self.flag, self.users, self.users_nicks, self.teams, self.order, self.index))
            elif True:
                if len(self.teams[0] + self.teams[1]) != pvp_settings.count_pick:
                    if self.label not in self.teams[self.flag]:
                        self.teams[self.flag].append(self.label)

                        # if self.flag == 0:
                        #     self.msg = self.msg.replace(f'\n\nВыбор игрока {self.users[1]}:', f'$\n\nВыбор игрока {self.users[1]}:').split('$')
                        # else:
                        #     self.msg = self.msg.replace('\n\nВыбирает покемона игрок', '$\n\nВыбирает покемона игрок').split('$')

                        self.index += 1
                        self.flag = self.order[self.index]

                        # self.msg[0] += ' ' + self.label
                        # if self.index != len(self.order) - 1 and self.index != len(self.order) - 2:
                        #     self.msg[0] += ','
                        # else:
                        #     self.msg[0] += '.'
                        # self.msg = ''.join(self.msg)

                        self.msg = self.msg[:self.msg.find('Выбирает покемона игрок') - 1]
                        if len(self.teams[0] + self.teams[1]) != pvp_settings.count_pick:
                            self.msg += '\n' + f'Выбирает покемона игрок {self.users[self.flag]}'

                    if len(self.teams[0] + self.teams[1]) != pvp_settings.count_pick:
                        for i in Pokemons_PvP.list_1:
                            view.add_item(PvPButton(i, self.msg, self.flag, self.users, self.users_nicks, self.teams, self.order, self.index))
                    else:
                        all_pokemons = Pokemons_PvP.list_1 + Pokemons_PvP.list_2[:-1]
                        index = random.randint(0, len(all_pokemons) - 1)
                        random_pokemon = all_pokemons[index]
                        # self.msg += f'\nСлучайный покемон: {all_pokemons[index]}.\n'
                        # self.msg += '\nУдачной игры!'
                        msg_flag = 2
            else:
                msg_flag = 1
            if msg_flag == 0:
                msg = self.msg
                await interaction.response.edit_message(content=msg, view=view)
            elif msg_flag == 2:
                await interaction.message.delete()
                player_id = [i for i in self.users_nicks]
                pokemons = self.teams[0] + self.teams[1] + [random_pokemon]
                pokemons_id = [Pokemons_PvP.dick_pokemon_name[i] for i in pokemons]
                background = pvp_settings.overlay('bkgd0', pokemons_id[0], pokemons_id[1], pokemons_id[2], player_id[0], player_id[1], pokemons[0], pokemons[1], pokemons[2])
                name = str(time.time())
                background.save(f'files_pvp/tmp/{name}.png')
                files = [discord.File(f'files_pvp/tmp/{name}.png')]
                os.remove(f'files_pvp/tmp/{name}.png')

                #await interaction.message.delete()

                channel = interaction.client.get_channel(interaction.channel_id)
                await channel.send(self.msg, view=view, files=files)
            else:
                await interaction.response.defer()
        else:
            await interaction.response.defer()
