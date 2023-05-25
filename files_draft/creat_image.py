from PIL import Image, ImageDraw, ImageFont
import discord
import os
import files_draft.Pokemons as Pokemons
import time

def overlay(bkgd, nick_1, nick_2, list_ban, list_pick_1, list_pick_2):
    background = Image.open(f'files_draft/image_pokemons/{bkgd}.png')

    ban_coordinates = [(740, 840), (840, 840), (980, 840), (1080, 840)]

    for i in range(len(ban_coordinates)):
        tmp = Image.open(f'files_draft/image_pokemons/ban/{list_ban[i]}.png')
        background.paste(tmp, ban_coordinates[i],  tmp)

    pick_1_coordinates = [(250, 130), (480, 180), (50, 450), (280, 500), (510, 550)]
    pick_2_coordinates = [(1460, 130), (1230, 180), (1660, 450), (1430, 500), (1200, 550)]

    for i in range(len(pick_1_coordinates)):
        tmp_1 = Image.open(f'files_draft/image_pokemons/pick/{list_pick_1[i]}.png')
        tmp_2 = Image.open(f'files_draft/image_pokemons/pick/{list_pick_2[i]}.png')

        background.paste(tmp_1, pick_1_coordinates[i],  tmp_1)
        background.paste(tmp_2, pick_2_coordinates[i],  tmp_2)


    font = ImageFont.truetype("files_draft/image_pokemons/Pokemon.ttf", 70)
    drawer = ImageDraw.Draw(background)

    list_of_words = [[-15, 850, ' ' * ((21 - len(nick_1)) // 2) + nick_1], [1320, 850, ' ' * ((22 - len(nick_2)) // 2) + nick_2]]

    for x, y, text in list_of_words:
        offset = 4
        shadowColor = (0, 0, 0)
        for off in range(offset):
            drawer.text((x-off, y), text, font=font, fill=shadowColor)
            drawer.text((x+off, y), text, font=font, fill=shadowColor)
            drawer.text((x, y+off), text, font=font, fill=shadowColor)
            drawer.text((x, y-off), text, font=font, fill=shadowColor)
            drawer.text((x-off, y+off), text, font=font, fill=shadowColor)
            drawer.text((x+off, y+off), text, font=font, fill=shadowColor)
            drawer.text((x-off, y-off), text, font=font, fill=shadowColor)
            drawer.text((x+off, y-off), text, font=font, fill=shadowColor)

        drawer.text((x, y), text, font=font, fill="#ffffff")

    return background

def creat_image(msg, nicks):
    msg = msg.replace(' ', '')

    nick_1, nick_2 = nicks

    ban = msg[msg.find('Баны:') + len('Баны:'):]
    list_ban = ban[:ban.find('.')].split(',')
    list_ban = [Pokemons.translate_pokemons_ru_eu[i] for i in list_ban]

    picks = msg[msg.find('Пиккоманды') + len('Пиккоманды'):]
    picks = picks[picks.find(':') + len(':'):].split('.')

    list_pick_1 = picks[0].split(',')
    list_pick_1 = [Pokemons.translate_pokemons_ru_eu[i] for i in list_pick_1]

    pick_2 = picks[1]
    list_pick_2 = pick_2[pick_2.find(':') + len(':'):].split(',')
    list_pick_2 = [Pokemons.translate_pokemons_ru_eu[i] for i in list_pick_2]

    background = overlay('bkgd', nick_1, nick_2, list_ban, list_pick_1, list_pick_2)
    name = nick_1 + nick_2 + str(time.time())
    background.save(f'files_draft/tmp/{name}.png')
    files = [discord.File(f'files_draft/tmp/{name}.png')]
    os.remove(f'files_draft/tmp/{name}.png')

    return files


def creat_image_eu(msg, nicks):
    msg = msg.replace(' ', '')

    nick_1, nick_2 = nicks

    ban = msg[msg.find('Bans:') + len('Bans:'):]
    list_ban = ban[:ban.find('.')].split(',')
    # list_ban = [Pokemons.translate_pokemons_ru_eu[i] for i in list_ban]

    picks = msg[msg.find('Peakteam') + len('Peakteam'):]
    picks = picks[picks.find(':') + len(':'):].split('.')

    list_pick_1 = picks[0].split(',')
    # list_pick_1 = [Pokemons.translate_pokemons_ru_eu[i] for i in list_pick_1]

    pick_2 = picks[1]
    list_pick_2 = pick_2[pick_2.find(':') + len(':'):].split(',')
    # list_pick_2 = [Pokemons.translate_pokemons_ru_eu[i] for i in list_pick_2]

    background = overlay('bkgd', nick_1, nick_2, list_ban, list_pick_1, list_pick_2)
    name = nick_1 + nick_2 + str(time.time())
    background.save(f'files_draft/tmp/{name}.png')
    files = [discord.File(f'files_draft/tmp/{name}.png')]
    os.remove(f'files_draft/tmp/{name}.png')

    return files
