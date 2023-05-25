from discord.ext import commands, tasks
from discord.ui import Button, View
import discord
import random
import requests
from PIL import Image
from io import BytesIO, StringIO
import os
import time
import files_rps.info_pokemon as info_pokemon
import files_rps.Pokemon as Pokemon
import files_rps.rps_settings as rps_settings
import files_rps.rps_pokemons as rps_pokemons
import database.database as database

class RPSButton(Button):
    def __init__(self, label, msg, game, evolution, creator_id, player_2_id, flag):
        if label in rps_settings.list_1:
            if label == 'Трава':
                style = discord.ButtonStyle.green
                self.type_pokemon = 0
            elif label == 'Огонь':
                style = discord.ButtonStyle.red
                self.type_pokemon = 1
            elif label == 'Вода':
                style = discord.ButtonStyle.blurple
                self.type_pokemon = 2
        elif label in rps_settings.list_2:
            if label == 'Ещё раз':
                style = discord.ButtonStyle.green
            elif label == 'Закончить':
                style = discord.ButtonStyle.red

        super().__init__(label=label, style=style)
        self.label = label
        self.msg = msg
        self.game = game
        self.evolution = evolution
        self.creator_id = creator_id
        self.player_2_id = player_2_id
        self.flag = flag

    async def callback(self, interaction):
        view = View(timeout=60*60)
        if self.label in rps_settings.list_1 and str(interaction.user.id) not in self.game.keys():
            await interaction.response.defer()
            if str(interaction.user.id) == self.creator_id and self.flag == 0:
                self.flag = 1
                if len(self.game) == 0:
                    self.evolution = random.randint(0, 2)

                id_pokemon = random.randint(0, len(rps_pokemons.list_pokemon[self.evolution][self.type_pokemon]) - 1)
                pokemon_id = rps_pokemons.list_pokemon[self.evolution][self.type_pokemon][id_pokemon]

                poke_info = info_pokemon.pokemon_input(str(pokemon_id))
                poke_name = rps_pokemons.dick_pokemon_name[poke_info[1]]

                if pokemon_id < 10:
                    pokemon_id = '00' + str(pokemon_id)
                elif pokemon_id < 100:
                    pokemon_id = '0' + str(pokemon_id)
                else:
                    pokemon_id = str(pokemon_id)

                self.game[str(interaction.user.id)] = [self.type_pokemon, poke_name, pokemon_id, str(interaction.user)[:-5]]

                if len(self.game) == 1:
                    self.msg = f'Тренер <@{str(interaction.user.id)}> выбрал покемона и ждет противника.\n'
                    if self.player_2_id != '':
                        self.msg = f'Тренер <@{str(interaction.user.id)}> выбрал покемона и ждет <@{self.player_2_id}>.\n'

                    for i in rps_settings.list_1:
                        view.add_item(RPSButton(i, self.msg, self.game, self.evolution, self.creator_id, self.player_2_id, self.flag))

                    # await interaction.response.edit_message(content=self.msg, view=view)
                    await interaction.message.edit(content=self.msg, view=view)
            elif self.flag == 1 and (self.player_2_id == '' or self.player_2_id == str(interaction.user.id)):
                id_pokemon = random.randint(0, len(rps_pokemons.list_pokemon[self.evolution][self.type_pokemon]) - 1)
                pokemon_id = rps_pokemons.list_pokemon[self.evolution][self.type_pokemon][id_pokemon]

                poke_info = info_pokemon.pokemon_input(str(pokemon_id))
                poke_name = rps_pokemons.dick_pokemon_name[poke_info[1]]

                if pokemon_id < 10:
                    pokemon_id = '00' + str(pokemon_id)
                elif pokemon_id < 100:
                    pokemon_id = '0' + str(pokemon_id)
                else:
                    pokemon_id = str(pokemon_id)

                self.game[str(interaction.user.id)] = [self.type_pokemon, poke_name, pokemon_id, str(interaction.user)[:-5]]

                player_id = [i for i in self.game]
                self.msg = self.msg[:self.msg.find('Тренер')]
                # self.msg = self.msg.replace('покемона', self.game[player_id[0]][1])
                # self.msg += f'Тренер <@{str(interaction.user.id)}> выбрал {self.game[player_id[1]][1]}.\n'

                if len(self.game) == 2:
                    player_id = [i for i in self.game]
                    game_result = rps_settings.check_winner(self.game[player_id[0]][0], self.game[player_id[1]][0])

                    background = rps_settings.overlay('bkgd' + str(game_result), self.game[player_id[0]][2], self.game[player_id[1]][2], self.game[player_id[0]][3], self.game[player_id[1]][3], self.game[player_id[0]][1], self.game[player_id[1]][1])
                    name = str(time.time())
                    background.save(f'files_rps/tmp/{name}.png')
                    files = [discord.File(f'files_rps/tmp/{name}.png')]
                    os.remove(f'files_rps/tmp/{name}.png')

                    database.game_over(self.game, game_result)

                    for i in rps_settings.list_2:
                        view.add_item(RPSButton(i, self.msg, self.game, self.evolution, self.creator_id, self.player_2_id, self.flag))

                    await interaction.message.delete()

                    channel = interaction.client.get_channel(interaction.channel_id)
                    await channel.send(self.msg, view=view, files=files)

        elif self.label in rps_settings.list_2 and str(interaction.user.id) == self.creator_id:
            if self.label == 'Ещё раз':
                self.msg = f'Создатель <@{self.creator_id}>.\nВыберите тип и дождитесь противника.\n'
                if self.player_2_id != '':
                    self.msg = f'Создатель <@{self.creator_id}>.\nВыберите тип и дождитесь <@{self.player_2_id}>.\n'
                for i in rps_settings.list_1:
                    view.add_item(RPSButton(i, self.msg, {}, '', self.creator_id, self.player_2_id, 0))

                await interaction.response.send_message(self.msg, view=view)
                await interaction.message.delete()

            elif self.label == 'Закончить':
                self.msg = self.msg.replace('\nПовторить игру?', '')
                await interaction.response.edit_message(content=self.msg, view=view)

        else:
            await interaction.response.defer()
