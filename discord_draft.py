import random

import discord
from discord.ext import commands, tasks
from discord.ui import Button, View

import files_draft.Pokemons as Pokemons
from files_draft.Buttons import ReadyButton, ReadyButton_eu
import files_draft.draft_settings as draft_settings

import files_team.name_buttons as name_buttons
from files_team.Buttons import TeamButton

import files_pvp.Pokemons_PvP as Pokemons_PvP
import files_pvp.pvp_settings as pvp_settings
from files_pvp.Buttons import PvPButton

from files_wheel_fortune.categories import categories
from files_wheel_fortune.phrases import single_phrases, double_phrases

import files_rps.rps_settings as rps_settings
from files_rps.Buttons import RPSButton

import files_roles.roles_buttons as roles_buttons
from files_roles.Buttons import RolesButton

import files_random_pvp.random_pvp as random_pvp

import database.database as database

token_test = ''
token_main = ''
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('ready')

@bot.command(name='драфт', help='Командный выбор покемонов с системой банов. Пример !драфт @gIDOHXypqh4y#7327')
async def draft(ctx, *, message=''):
    user_1 = str(ctx.message.author.mention)
    user_2 = message[message.find('<@'):message.find('>') + 1]

    if user_2 != '' and user_1 != user_2:
        msg = f'Драфт между командами {user_1} и {user_2}.\nКапитан {user_1} выбирает КОЛИЧЕСТВО банов.'
        view = View(timeout=60*60)
        for i in Pokemons.list_0:
            view.add_item(ReadyButton(i, msg, 0, [user_1, user_2], [], [[], []], [], 0, 0, True, 0, [], 1))

        message = await ctx.send(msg, view=view)

@bot.command(name='draft', help='Team selection of Pokemon with a system of bans. Example !draft @gIDOHXypqh4y#7327')
async def draft(ctx, *, message=''):
    user_1 = str(ctx.message.author.mention)
    user_2 = message[message.find('<@'):message.find('>') + 1]

    if user_2 != '' and user_1 != user_2:
        # msg = f'Draft between teams {user_1} and {user_2}.\nCaptain {user_1} selects the NUMBER of bans.'
        msg = f'Draft between teams {user_1} and {user_2}.\nNumber of bans: 4.\nPokemon are unique for two teams.\nBans:\n\nPeak team {user_1}:\n\nPeak team {user_2}:\n\nSelects a Pokemon to BAN the team {user_1}'
        view = View(timeout=60*60)
        for i in Pokemons.list_1_eu: #list_0
            # view.add_item(ReadyButton_eu(i, msg, 0, [user_1, user_2], [], [[], []], [], 0, 0, True, 0, []))
            view.add_item(ReadyButton_eu(i, msg, 0, [user_1, user_2], [], [[], []], draft_settings.ban_pick[3], 0, 4, True, 1, []))

        message = await ctx.send(msg, view=view)

@bot.command(name='колесо', help='Случайный выбор покемонов с одинаковыми признаками. Пример !колесо или !колесо @gIDOHXypqh4y#7327')
async def wheel_fortune(ctx, *, message=''):
    type_rnd = random.choice(list(categories.keys()))
    response = type_rnd + ': ' + ', '.join(categories[type_rnd])

    chance_of_azumarill = 5
    additional_text = str()

    user_1 = str(ctx.message.author.mention)
    user_2 = message[message.find('<@'):message.find('>') + 1]

    if user_2 != '':
        phrase = random.choice(double_phrases).format(user_1=user_1, user_2=user_2)

        if random.randint(0, 100) <= chance_of_azumarill:
            additional_text = 'P.S. Настало время быть на подсосе - обязательный пик Базвола в обоих командах.'

        msg = f'{phrase}\n{response}.\n{additional_text}'
    else:
        phrase = random.choice(single_phrases).format(user_1=user_1)

        if random.randint(0, 100) <= chance_of_azumarill:
            additional_text = 'P.S. Настало время быть на подсосе - обязательный пик Базвола.'

        msg = f'{phrase}\n{response}.\n{additional_text}'

    message = await ctx.send(msg)

@bot.command(name='кнб', help='Кнб на лад покемонов')
async def rps(ctx, *, message=''):
    user_1 = str(ctx.message.author.mention)
    user_2 = message[message.find('<@'):message.find('>') + 1][:-1][2:]

    msg = f'Создатель {user_1}.\nВыберите тип и дождитесь противника.\n'
    if user_2 != '':
        msg = f'Создатель {user_1}.\nВыберите тип и дождитесь <@{user_2}>.\n'

    view = View(timeout=15*60)
    for i in rps_settings.list_1:
        view.add_item(RPSButton(i, msg, {}, '', user_1[:-1][2:], user_2, 0))

    message = await ctx.send(msg, view=view)

@bot.command(name='топ', help='Топ игроков кнб')
async def top(ctx, *, message=''):
    user_1 = int(ctx.message.author.id)
    msg = database.get_top_rps(user_1)
    message = await ctx.send(msg)

@bot.command(name='team', help='')
async def team(ctx, *, message=''):
    user_1 = str(ctx.message.author.mention)
    msg = f'{user_1}, выберите количество человек.'
    count_players = message.count('<@') + 1
    if '<@' in message:
        msg += 'Играют:\n' + message.replace(' ', '').replace('<@', '\n<@')

    view = View(timeout=60*60)
    for i in name_buttons.list_0:
        view.add_item(TeamButton(i, msg, count_players, 0, user_1))

    message = await ctx.send(msg, view=view)

@bot.command(name='pvp', help='Example !pvp @gIDOHXypqh4y#7327')
async def draft(ctx, *, message=''):
    user_1 = str(ctx.message.author.mention)
    user_2 = message[message.find('<@'):message.find('>') + 1]
    if user_2 != '':
        msg = f'Пвп между капитанами {user_1} и {user_2}.\n\nВыбирает покемона игрок {user_1}' #\n\nВыбор игрока {user_1}:\n\nВыбор игрока {user_2}:
        view = View(timeout=60*60)
        for i in Pokemons_PvP.list_1:
            view.add_item(PvPButton(i, msg, 0, [user_1, user_2], [], [[], []], pvp_settings.ban_pick[0], 0))

        message = await ctx.send(msg, view=view)

@bot.command(name='рандом', help='Example !pvp @gIDOHXypqh4y#7327')
async def func_random_pvp(ctx, *, message=''):
    user_1 = str(ctx.message.author.mention)
    user_2 = message[message.find('<@'):message.find('>') + 1]
    if user_2 != '':
        msg = random_pvp.random_pvp(user_1, user_2)
        message = await ctx.send(msg)

# @bot.command(name='roles', help='')
# async def roles(ctx, *, message=''):
#     for role in roles_buttons.all_list:
#         view = View(timeout=365*24*60*60)
#         msg = role[0]
#         for i in role[2]:
#             view.add_item(RolesButton(i, msg, role[1]))
#
#         message = await ctx.send(msg, view=view)

# @bot.command(name='test', help='')
# async def test(ctx, *, message=''):
#     msg = message
#     print(message)
#     # print(dir(ctx))
#     # print(ctx.attachments)
#     # if message.attachments:
#     #     files = list()
#     #     for attachment in message.attachments:
#     #         files.append(await attachment.to_file())
#     #     if files:
#     #         message = await ctx.send(message, files=files)


# @bot.command(name='qqq', help='Team selection of Pokemon with a system of bans. Example !draft @gIDOHXypqh4y#7327')
# async def draft(ctx, *, message=''):
#     print(bot.guilds)
# @bot.command(name='change',  help='')
# async def rename(ctx, *, message=''):
#     print(bot.guilds)
#     await bot.guilds[4].get_member(976431385164283915).edit(nick='Toxic_Family_Bot')

bot.run(token_main)
