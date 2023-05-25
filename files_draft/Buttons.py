from discord.ext import commands, tasks
from discord.ui import Button, View
import discord
import files_draft.draft_settings as draft_settings
import files_draft.Pokemons as Pokemons
import files_draft.creat_image as creat_image

class ReadyButton(Button):
    def __init__(self, label, msg, flag, users, ban_list, teams, order, index, count_ban, pokemon_replay, game_flag, users_nicks, page_now):
        style = discord.ButtonStyle.green
        if game_flag == 0 or count_ban != 6:
            if order != draft_settings.ban_pick[4]:
                if label in ban_list or label in teams[flag]:
                    style = discord.ButtonStyle.red
                elif label == '<-' or label == '->':
                    style = discord.ButtonStyle.blurple
            elif order == draft_settings.ban_pick[4]:
                if label in ban_list and len(ban_list) == count_ban:
                    style = discord.ButtonStyle.red
                if label in teams[flag]:
                    style = discord.ButtonStyle.red
                if label == '<-' or label == '->':
                    style = discord.ButtonStyle.blurple
        else:
            if len(ban_list) == count_ban:
                if label in ban_list or label in teams[flag]:
                    style = discord.ButtonStyle.red
                elif label == '<-' or label == '->':
                    style = discord.ButtonStyle.blurple
            else:
                if label in ban_list or label in teams[0] + teams[1]:
                    style = discord.ButtonStyle.red
                elif label == '<-' or label == '->':
                    style = discord.ButtonStyle.blurple



        super().__init__(label=label, style=style)
        self.label = label
        self.msg = msg
        self.flag = flag
        self.users = users
        self.ban_list = ban_list
        self.teams = teams
        self.order = order
        self.index = index
        self.count_ban = count_ban
        self.pokemon_replay = pokemon_replay
        self.game_flag = game_flag
        self.users_nicks = users_nicks
        self.page_now = page_now

    async def callback(self, interaction):
        view = View(timeout=60*60)
        msg_flag = 0

        if str(interaction.user.id) in self.users[self.flag]:
            if str(interaction.user)[:-5] not in self.users_nicks:
                self.users_nicks.append(str(interaction.user)[:-5])

            if str(interaction.user.id) in self.users[0] and self.label in Pokemons.list_0:
                if self.label == Pokemons.list_0[3]:
                    self.game_flag = 1
                    self.count_ban = 4
                    self.order = draft_settings.ban_pick[3]
                elif self.label == Pokemons.list_0[4]:
                    self.count_ban = 2
                    self.order = draft_settings.ban_pick[4]
                else:
                    self.count_ban = int(self.label) * 2
                    self.order = draft_settings.ban_pick[self.count_ban // 2]

                self.msg = f'Драфт между командами {self.users[0]} и {self.users[1]}.\nКоличество банов: {self.count_ban}.\n\n{self.users[0]}, покемоны в драфте уникальны?'

                for i in Pokemons.list_00:
                    view.add_item(ReadyButton(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay, self.game_flag, self.users_nicks, self.page_now))
            elif str(interaction.user.id) in self.users[0] and self.label in Pokemons.list_00:
                self.pokemon_replay = self.label == Pokemons.list_00[0]

                if self.count_ban != 0:
                    if self.pokemon_replay:
                        self.msg = f'Драфт между командами {self.users[0]} и {self.users[1]}.\nКоличество банов: {self.count_ban}.\nПокемоны уникальны для двух команд.\nБаны:\n\nПик команды {self.users[0]}:\n\nПик команды {self.users[1]}:\n\nВыбирает покемона для БАНА команда {self.users[0]}'
                    else:
                        self.msg = f'Драфт между командами {self.users[0]} и {self.users[1]}.\nКоличество банов: {self.count_ban}.\nПокемоны могут повторяться.\nБаны:\n\nПик команды {self.users[0]}:\n\nПик команды {self.users[1]}:\n\nВыбирает покемона для БАНА команда {self.users[0]}'
                else:
                    if self.pokemon_replay:
                        self.msg = f'Драфт между командами {self.users[0]} и {self.users[1]}.\nКоличество банов: 0.\nПокемоны уникальны для двух команд.\n\nПик команды {self.users[0]}:\n\nПик команды {self.users[1]}:\n\nВыбирает покемона команда {self.users[0]}'
                    else:
                        self.msg = f'Драфт между командами {self.users[0]} и {self.users[1]}.\nКоличество банов: 0.\nПокемоны могут повторяться.\n\nПик команды {self.users[0]}:\n\nПик команды {self.users[1]}:\n\nВыбирает покемона команда {self.users[0]}'

                self.page_now = 1
                for i in Pokemons.list_1:
                    view.add_item(ReadyButton(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay, self.game_flag, self.users_nicks, self.page_now))
            elif self.label == '->':
                if self.page_now == 1:
                    self.page_now = 2
                    for i in Pokemons.list_2:
                        view.add_item(ReadyButton(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay, self.game_flag, self.users_nicks, self.page_now))
                elif self.page_now == 2:
                    self.page_now = 3
                    for i in Pokemons.list_3:
                        view.add_item(ReadyButton(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay, self.game_flag, self.users_nicks, self.page_now))
            elif self.label == '<-':
                if self.page_now == 2:
                    self.page_now = 1
                    for i in Pokemons.list_1:
                        view.add_item(ReadyButton(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay, self.game_flag, self.users_nicks, self.page_now))
                elif self.page_now == 3:
                    self.page_now = 2
                    for i in Pokemons.list_2:
                        view.add_item(ReadyButton(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay, self.game_flag, self.users_nicks, self.page_now))
            elif self.label not in self.ban_list or (len(self.ban_list) != self.count_ban and self.order == draft_settings.ban_pick[4]):

                if len(self.ban_list) != self.count_ban:
                    if self.game_flag == 0:
                        self.ban_list.append(self.label)
                        self.index += 1
                        self.flag = self.order[self.index]

                        if self.order != draft_settings.ban_pick[4]:
                            self.msg = self.msg.replace(f'\n\nПик команды {self.users[0]}:', f'$\n\nПик команды {self.users[0]}:').split('$')
                            self.msg[0] += ' ' + self.label

                            if len(self.ban_list) != self.count_ban:
                                self.msg[0] += ','
                            else:
                                self.msg[0] += '.'

                            self.msg = ''.join(self.msg)
                        elif self.order == draft_settings.ban_pick[4] and len(self.ban_list) == self.count_ban:
                            self.msg = self.msg.replace(f'\n\nПик команды {self.users[0]}:', f'$\n\nПик команды {self.users[0]}:').split('$')
                            self.msg[0] += ' ' + self.ban_list[0] + ', ' + self.ban_list[1] + '.'
                            self.msg = ''.join(self.msg)

                        self.msg = self.msg[:self.msg.find('Выбирает покемона для БАНА команда') - 1]
                        if len(self.ban_list) != self.count_ban:
                            self.msg += '\n' + f'Выбирает покемона для БАНА команда {self.users[self.flag]}'
                        else:
                            self.msg += '\n' + f'Выбирает покемона команда {self.users[self.flag]}'
                        self.page_now = 1
                        for i in Pokemons.list_1:
                            view.add_item(ReadyButton(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay, self.game_flag, self.users_nicks, self.page_now))
                    elif self.label not in self.teams[0] and self.label not in self.teams[1]:
                        self.ban_list.append(self.label)
                        self.index += 1
                        self.flag = self.order[self.index]

                        self.msg = self.msg.replace(f'\n\nПик команды {self.users[0]}:', f'$\n\nПик команды {self.users[0]}:').split('$')
                        self.msg[0] += ' ' + self.label

                        loc_count_ban = 4
                        if self.pokemon_replay:
                            loc_count_ban = 10

                        if len(self.ban_list) != loc_count_ban:
                            self.msg[0] += ','
                        else:
                            self.msg[0] += '.'
                        self.msg = ''.join(self.msg)

                        self.msg = self.msg[:self.msg.find('Выбирает покемона для БАНА команда') - 1]


                        if len(self.ban_list) != self.count_ban - 2:
                            self.msg += '\n' + f'Выбирает покемона для БАНА команда {self.users[self.flag]}'
                        else:
                            self.ban_list.append(-1)
                            self.ban_list.append(-1)
                            self.msg += '\n' + f'Выбирает покемона команда {self.users[self.flag]}'
                        self.page_now = 1
                        for i in Pokemons.list_1:
                            view.add_item(ReadyButton(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay, self.game_flag, self.users_nicks, self.page_now))
                    else:
                        msg_flag = 1

                elif len(self.ban_list) == self.count_ban and len(self.teams[0] + self.teams[1]) != draft_settings.count_pick:
                    if self.game_flag == 0:
                        if self.label not in self.teams[self.flag]:
                            if self.pokemon_replay:
                                self.ban_list.append(self.label)
                                self.count_ban += 1
                            self.teams[self.flag].append(self.label)

                            if self.flag == 0:
                                self.msg = self.msg.replace(f'\n\nПик команды {self.users[1]}:', f'$\n\nПик команды {self.users[1]}:').split('$')
                            else:
                                self.msg = self.msg.replace('\n\nВыбирает покемона команда', '$\n\nВыбирает покемона команда').split('$')

                            self.index += 1
                            self.flag = self.order[self.index]

                            self.msg[0] += ' ' + self.label
                            if self.index != len(self.order) - 1 and self.index != len(self.order) - 2:
                                self.msg[0] += ','
                            else:
                                self.msg[0] += '.'
                            self.msg = ''.join(self.msg)

                            self.msg = self.msg[:self.msg.find('Выбирает покемона команда') - 1]
                            if len(self.teams[0] + self.teams[1]) != draft_settings.count_pick:
                                self.msg += '\n' + f'Выбирает покемона команда {self.users[self.flag]}'

                        if len(self.ban_list) == self.count_ban and len(self.teams[0] + self.teams[1]) != draft_settings.count_pick:
                            self.page_now = 1
                            for i in Pokemons.list_1:
                                view.add_item(ReadyButton(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay, self.game_flag, self.users_nicks, self.page_now))
                        else:
                            self.ban_list = list()
                            self.msg += '\nУдачной игры!'
                    else:
                        if self.label not in self.teams[self.flag]:
                            if self.pokemon_replay:
                                self.ban_list.append(self.label)
                                self.count_ban += 1
                            self.teams[self.flag].append(self.label)

                            if self.flag == 0:
                                self.msg = self.msg.replace(f'\n\nПик команды {self.users[1]}:', f'$\n\nПик команды {self.users[1]}:').split('$')
                            else:
                                self.msg = self.msg.replace('\n\nВыбирает покемона команда', '$\n\nВыбирает покемона команда').split('$')

                            self.index += 1
                            self.flag = self.order[self.index]

                            self.msg[0] += ' ' + self.label
                            if self.index != len(self.order) - 1 and self.index != len(self.order) - 2:
                                self.msg[0] += ','
                            else:
                                self.msg[0] += '.'
                            self.msg = ''.join(self.msg)

                            self.msg = self.msg[:self.msg.find('Выбирает покемона команда') - 1]
                            if len(self.teams[0] + self.teams[1]) != 6:
                                if len(self.teams[0] + self.teams[1]) != draft_settings.count_pick:
                                    self.msg += '\n' + f'Выбирает покемона команда {self.users[self.flag]}'
                            else:
                                del self.ban_list[self.ban_list.index(-1)]
                                del self.ban_list[self.ban_list.index(-1)]
                                self.count_ban += 2
                                self.msg += '\n' + f'Выбирает покемона для БАНА команда {self.users[self.flag]}'

                        if len(self.teams[0] + self.teams[1]) != draft_settings.count_pick:
                            self.page_now = 1
                            for i in Pokemons.list_1:
                                view.add_item(ReadyButton(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay, self.game_flag, self.users_nicks, self.page_now))
                        else:
                            self.ban_list = list()
                            self.msg += '\nУдачной игры!'
            else:
                msg_flag = 1
            if msg_flag == 0:
                msg = self.msg
                await interaction.response.edit_message(content=msg, view=view)

                if 'Удачной игры!' in self.msg and self.game_flag == 1:
                    files = creat_image.creat_image(self.msg, self.users_nicks)
                    channel = interaction.client.get_channel(interaction.channel_id)
                    await channel.send(files=files) #channel.send(self.msg, files=files)
            else:
                await interaction.response.defer()
        else:
            await interaction.response.defer()



class ReadyButton_eu(Button):
    def __init__(self, label, msg, flag, users, ban_list, teams, order, index, count_ban, pokemon_replay, game_flag, users_nicks):
        style = discord.ButtonStyle.green
        if game_flag == 0 or count_ban != 6:
            if label in ban_list or label in teams[flag]:
                style = discord.ButtonStyle.red
            elif label == '<-' or label == '->':
                style = discord.ButtonStyle.blurple
        else:
            if len(ban_list) == count_ban:
                if label in ban_list or label in teams[flag]:
                    style = discord.ButtonStyle.red
                elif label == '<-' or label == '->':
                    style = discord.ButtonStyle.blurple
            else:
                if label in ban_list or label in teams[0] + teams[1]:
                    style = discord.ButtonStyle.red
                elif label == '<-' or label == '->':
                    style = discord.ButtonStyle.blurple

        super().__init__(label=label, style=style)
        self.label = label
        self.msg = msg
        self.flag = flag
        self.users = users
        self.ban_list = ban_list
        self.teams = teams
        self.order = order
        self.index = index
        self.count_ban = count_ban
        self.pokemon_replay = pokemon_replay
        self.game_flag = game_flag
        self.users_nicks = users_nicks

    async def callback(self, interaction):
        view = View(timeout=60*60)
        msg_flag = 0

        if str(interaction.user.id) in self.users[self.flag]:
            if str(interaction.user)[:-5] not in self.users_nicks:
                self.users_nicks.append(str(interaction.user)[:-5])

            if str(interaction.user.id) in self.users[0] and self.label in Pokemons.list_0:
                if self.label == Pokemons.list_0[-1]:
                    self.game_flag = 1
                    self.count_ban = 4
                    self.order = draft_settings.ban_pick[3]
                else:
                    self.count_ban = int(self.label) * 2
                    self.order = draft_settings.ban_pick[self.count_ban // 2]

                self.msg = f'Draft between teams {self.users[0]} and {self.users[1]}.\nNumber of bans: {self.count_ban}.\n\n{self.users[0]}, are Pokemon unique in the draft?'

                for i in Pokemons.list_00_eu:
                    view.add_item(ReadyButton_eu(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay, self.game_flag, self.users_nicks))
            elif str(interaction.user.id) in self.users[0] and self.label in Pokemons.list_00_eu:
                self.pokemon_replay = self.label == Pokemons.list_00_eu[0]

                if self.count_ban != 0:
                    if self.pokemon_replay:
                        self.msg = f'Draft between teams {self.users[0]} and {self.users[1]}.\nNumber of bans: {self.count_ban}.\nPokemon are unique for two teams.\nBans:\n\nPeak team {self.users[0]}:\n\nPeak team {self.users[1]}:\n\nSelects a Pokemon to BAN the team {self.users[0]}'
                    else:
                        self.msg = f'Draft between teams {self.users[0]} and {self.users[1]}.\nNumber of bans: {self.count_ban}.\nPokemon can be repeated.\nBans:\n\nPeak team {self.users[0]}:\n\nPeak team {self.users[1]}:\n\nSelects a Pokemon to BAN the team {self.users[0]}'
                else:
                    if self.pokemon_replay:
                        self.msg = f'Draft between teams {self.users[0]} and {self.users[1]}.\nNumber of bans: 0.\nPokemon are unique for two teams.\n\nPeak team {self.users[0]}:\n\nPeak team {self.users[1]}:\n\nThe Pokemon is chosen by the team {self.users[0]}'
                    else:
                        self.msg = f'Draft between teams {self.users[0]} and {self.users[1]}.\nNumber of bans: 0.\nPokemon can be repeated.\n\nPeak team {self.users[0]}:\n\nPeak team {self.users[1]}:\n\nThe Pokemon is chosen by the team {self.users[0]}'

                for i in Pokemons.list_1_eu:
                    view.add_item(ReadyButton_eu(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay, self.game_flag, self.users_nicks))
            elif self.label == '->':
                for i in Pokemons.list_2_eu:
                    view.add_item(ReadyButton_eu(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay, self.game_flag, self.users_nicks))
            elif self.label == '<-':
                for i in Pokemons.list_1_eu:
                    view.add_item(ReadyButton_eu(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay, self.game_flag, self.users_nicks))
            elif self.label not in self.ban_list:

                if len(self.ban_list) != self.count_ban:
                    if self.game_flag == 0:
                        self.ban_list.append(self.label)
                        self.index += 1
                        self.flag = self.order[self.index]

                        self.msg = self.msg.replace(f'\n\nPeak team {self.users[0]}:', f'$\n\nPeak team {self.users[0]}:').split('$')
                        self.msg[0] += ' ' + self.label

                        if len(self.ban_list) != self.count_ban:
                            self.msg[0] += ','
                        else:
                            self.msg[0] += '.'

                        self.msg = ''.join(self.msg)

                        self.msg = self.msg[:self.msg.find('Selects a Pokemon to BAN the team') - 1]
                        if len(self.ban_list) != self.count_ban:
                            self.msg += '\n' + f'Selects a Pokemon to BAN the team {self.users[self.flag]}'
                        else:
                            self.msg += '\n' + f'The Pokemon is chosen by the team {self.users[self.flag]}'

                        for i in Pokemons.list_1_eu:
                            view.add_item(ReadyButton_eu(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay, self.game_flag, self.users_nicks))
                    elif self.label not in self.teams[0] and self.label not in self.teams[1]:
                        self.ban_list.append(self.label)
                        self.index += 1
                        self.flag = self.order[self.index]

                        self.msg = self.msg.replace(f'\n\nPeak team {self.users[0]}:', f'$\n\nPeak team {self.users[0]}:').split('$')
                        self.msg[0] += ' ' + self.label

                        loc_count_ban = 4
                        if self.pokemon_replay:
                            loc_count_ban = 10

                        if len(self.ban_list) != loc_count_ban:
                            self.msg[0] += ','
                        else:
                            self.msg[0] += '.'
                        self.msg = ''.join(self.msg)

                        self.msg = self.msg[:self.msg.find('Selects a Pokemon to BAN the team') - 1]


                        if len(self.ban_list) != self.count_ban - 2:
                            self.msg += '\n' + f'Selects a Pokemon to BAN the team {self.users[self.flag]}'
                        else:
                            self.ban_list.append(-1)
                            self.ban_list.append(-1)
                            self.msg += '\n' + f'The Pokemon is chosen by the team {self.users[self.flag]}'

                        for i in Pokemons.list_1_eu:
                            view.add_item(ReadyButton_eu(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay, self.game_flag, self.users_nicks))
                    else:
                        msg_flag = 1

                elif len(self.ban_list) == self.count_ban and len(self.teams[0] + self.teams[1]) != draft_settings.count_pick:
                    if self.game_flag == 0:
                        if self.label not in self.teams[self.flag]:
                            if self.pokemon_replay:
                                self.ban_list.append(self.label)
                                self.count_ban += 1
                            self.teams[self.flag].append(self.label)

                            if self.flag == 0:
                                self.msg = self.msg.replace(f'\n\nPeak team {self.users[1]}:', f'$\n\nPeak team {self.users[1]}:').split('$')
                            else:
                                self.msg = self.msg.replace('\n\nThe Pokemon is chosen by the team', '$\n\nThe Pokemon is chosen by the team').split('$')

                            self.index += 1
                            self.flag = self.order[self.index]

                            self.msg[0] += ' ' + self.label
                            if self.index != len(self.order) - 1 and self.index != len(self.order) - 2:
                                self.msg[0] += ','
                            else:
                                self.msg[0] += '.'
                            self.msg = ''.join(self.msg)

                            self.msg = self.msg[:self.msg.find('The Pokemon is chosen by the team') - 1]
                            if len(self.teams[0] + self.teams[1]) != draft_settings.count_pick:
                                self.msg += '\n' + f'The Pokemon is chosen by the team {self.users[self.flag]}'

                        if len(self.ban_list) == self.count_ban and len(self.teams[0] + self.teams[1]) != draft_settings.count_pick:
                            for i in Pokemons.list_1_eu:
                                view.add_item(ReadyButton_eu(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay, self.game_flag, self.users_nicks))
                        else:
                            self.ban_list = list()
                            self.msg += '\nHave a good game!'
                    else:
                        if self.label not in self.teams[self.flag]:
                            if self.pokemon_replay:
                                self.ban_list.append(self.label)
                                self.count_ban += 1
                            self.teams[self.flag].append(self.label)

                            if self.flag == 0:
                                self.msg = self.msg.replace(f'\n\nPeak team {self.users[1]}:', f'$\n\nPeak team {self.users[1]}:').split('$')
                            else:
                                self.msg = self.msg.replace('\n\nThe Pokemon is chosen by the team', '$\n\nThe Pokemon is chosen by the team').split('$')

                            self.index += 1
                            self.flag = self.order[self.index]

                            self.msg[0] += ' ' + self.label
                            if self.index != len(self.order) - 1 and self.index != len(self.order) - 2:
                                self.msg[0] += ','
                            else:
                                self.msg[0] += '.'
                            self.msg = ''.join(self.msg)

                            self.msg = self.msg[:self.msg.find('The Pokemon is chosen by the team') - 1]
                            if len(self.teams[0] + self.teams[1]) != 6:
                                if len(self.teams[0] + self.teams[1]) != draft_settings.count_pick:
                                    self.msg += '\n' + f'The Pokemon is chosen by the team {self.users[self.flag]}'
                            else:
                                del self.ban_list[self.ban_list.index(-1)]
                                del self.ban_list[self.ban_list.index(-1)]
                                self.count_ban += 2
                                self.msg += '\n' + f'Selects a Pokemon to BAN the team {self.users[self.flag]}'

                        if len(self.teams[0] + self.teams[1]) != draft_settings.count_pick:
                            for i in Pokemons.list_1_eu:
                                view.add_item(ReadyButton_eu(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay, self.game_flag, self.users_nicks))
                        else:
                            self.ban_list = list()
                            self.msg += '\nHave a good game!'
            else:
                msg_flag = 1
            if msg_flag == 0:
                msg = self.msg
                await interaction.response.edit_message(content=msg, view=view)

                if 'Have a good game!' in self.msg and self.game_flag == 1:
                    files = creat_image.creat_image_eu(self.msg, self.users_nicks)
                    channel = interaction.client.get_channel(interaction.channel_id)
                    await channel.send(files=files) #channel.send(self.msg, files=files)
            else:
                await interaction.response.defer()
        else:
            await interaction.response.defer()




# class ReadyButton_eu(Button):
#     def __init__(self, label, msg, flag, users, ban_list, teams, order, index, count_ban, pokemon_replay):
#         style = discord.ButtonStyle.green
#         if label in ban_list or label in teams[flag]:
#             style = discord.ButtonStyle.red
#         elif label == '<-' or label == '->':
#             style = discord.ButtonStyle.blurple
#
#         super().__init__(label=label, style=style)
#         self.label = label
#         self.msg = msg
#         self.flag = flag
#         self.users = users
#         self.ban_list = ban_list
#         self.teams = teams
#         self.order = order
#         self.index = index
#         self.count_ban = count_ban
#         self.pokemon_replay = pokemon_replay
#
#     async def callback(self, interaction):
#         view = View(timeout=60*60)
#         msg_flag = 0
#         if str(interaction.user.id) in self.users[self.flag]:
#             if str(interaction.user.id) in self.users[0] and self.label in Pokemons.list_0:
#                 self.count_ban = int(self.label) * 2
#                 self.order = draft_settings.ban_pick[self.count_ban // 2]
#
#                 self.msg = f'Draft between captains {self.users[0]} и {self.users[1]}.\nNumber of bans: {self.count_ban}.\n\n{self.users[0]}, are Pokémon drafted unique?'
#
#                 for i in Pokemons.list_00_eu:
#                     view.add_item(ReadyButton_eu(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay))
#             elif str(interaction.user.id) in self.users[0] and self.label in Pokemons.list_00_eu:
#                 self.pokemon_replay = self.label == Pokemons.list_00_eu[0]
#
#                 if self.count_ban != 0:
#                     if self.pokemon_replay:
#                         self.msg = f'Draft between captains {self.users[0]} и {self.users[1]}.\nNumber of bans: {self.count_ban}.\nPokémon are unique to the two teams.\nBans:\n\nSelected Pokémon {self.users[0]}:\n\nSelected Pokémon {self.users[1]}:\n\nSelect Pokémon for BAN {self.users[0]}'
#                     else:
#                         self.msg = f'Draft between captains {self.users[0]} и {self.users[1]}.\nNumber of bans: {self.count_ban}.\nPokémon are not unique to the two teams.\nBans:\n\nSelected Pokémon {self.users[0]}:\n\nSelected Pokémon {self.users[1]}:\n\nSelect Pokémon for BAN {self.users[0]}'
#                 else:
#                     if self.pokemon_replay:
#                         self.msg = f'Draft between captains {self.users[0]} и {self.users[1]}.\nNumber of bans: 0.\nPokémon are unique to the two teams.\n\nSelected Pokémon {self.users[0]}:\n\nSelected Pokémon {self.users[1]}:\n\nSelect Pokémon captain {self.users[0]}'
#                     else:
#                         self.msg = f'Draft between captains {self.users[0]} и {self.users[1]}.\nNumber of bans: 0.\nPokémon are not unique to the two teams.\n\nSelected Pokémon {self.users[0]}:\n\nSelected Pokémon {self.users[1]}:\n\nSelect Pokémon captain {self.users[0]}'
#
#                 for i in Pokemons.list_1_eu:
#                     view.add_item(ReadyButton_eu(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay))
#             elif self.label == '->':
#                 for i in Pokemons.list_2_eu:
#                     view.add_item(ReadyButton_eu(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay))
#             elif self.label == '<-':
#                 for i in Pokemons.list_1_eu:
#                     view.add_item(ReadyButton_eu(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay))
#             elif self.label not in self.ban_list:
#                 if len(self.ban_list) != self.count_ban:
#                     self.ban_list.append(self.label)
#                     self.index += 1
#                     self.flag = self.order[self.index]
#
#                     self.msg = self.msg.replace(f'\n\nSelected Pokémon {self.users[0]}:', f'$\n\nSelected Pokémon {self.users[0]}:').split('$')
#                     self.msg[0] += ' ' + self.label
#                     if len(self.ban_list) != self.count_ban:
#                         self.msg[0] += ','
#                     else:
#                         self.msg[0] += '.'
#                     self.msg = ''.join(self.msg)
#
#                     self.msg = self.msg[:self.msg.find('Select Pokémon for BAN') - 1]
#                     if len(self.ban_list) != self.count_ban:
#                         self.msg += '\n' + f'Select Pokémon for BAN {self.users[self.flag]}'
#                     else:
#                         self.msg += '\n' + f'Select Pokémon captain {self.users[self.flag]}'
#
#                     for i in Pokemons.list_1_eu:
#                         view.add_item(ReadyButton_eu(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay))
#
#                 elif len(self.ban_list) == self.count_ban and len(self.teams[0] + self.teams[1]) != draft_settings.count_pick:
#                     if self.label not in self.teams[self.flag]:
#                         if self.pokemon_replay:
#                             self.ban_list.append(self.label)
#                             self.count_ban += 1
#                         self.teams[self.flag].append(self.label)
#
#                         if self.flag == 0:
#                             self.msg = self.msg.replace(f'\n\nSelected Pokémon {self.users[1]}:', f'$\n\nSelected Pokémon {self.users[1]}:').split('$')
#                         else:
#                             self.msg = self.msg.replace('\n\nSelect Pokémon captain', '$\n\nSelect Pokémon captain').split('$')
#
#                         self.index += 1
#                         self.flag = self.order[self.index]
#
#                         self.msg[0] += ' ' + self.label
#                         if self.index != len(self.order) - 1 and self.index != len(self.order) - 2:
#                             self.msg[0] += ','
#                         else:
#                             self.msg[0] += '.'
#                         self.msg = ''.join(self.msg)
#
#                         self.msg = self.msg[:self.msg.find('Select Pokémon captain') - 1]
#                         if len(self.teams[0] + self.teams[1]) != draft_settings.count_pick:
#                             self.msg += '\n' + f'Select Pokémon captain {self.users[self.flag]}'
#
#                     if len(self.ban_list) == self.count_ban and len(self.teams[0] + self.teams[1]) != draft_settings.count_pick:
#                         for i in Pokemons.list_1_eu:
#                             view.add_item(ReadyButton_eu(i, self.msg, self.flag, self.users, self.ban_list, self.teams, self.order, self.index, self.count_ban, self.pokemon_replay))
#                     else:
#                         self.ban_list = list()
#                         self.msg += '\nGood luck!'
#             else:
#                 msg_flag = 1
#             if msg_flag == 0:
#                 msg = self.msg
#                 await interaction.response.edit_message(content=msg, view=view)
#             else:
#                 await interaction.response.defer()
#         else:
#             await interaction.response.defer()
