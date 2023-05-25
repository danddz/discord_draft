list_1 = ['Трава', 'Огонь', 'Вода']
list_2 = ['Ещё раз', 'Закончить']

def check_winner(type_1, type_2):
    if type_1 == type_2:
        return 0

    if type_1 == 2 and type_2 == 1:
        return 1
    if type_1 == 2 and type_2 == 0:
        return 2

    if type_1 == 1 and type_2 == 0:
        return 1
    if type_1 == 1 and type_2 == 2:
        return 2

    if type_1 == 0 and type_2 == 2:
        return 1
    if type_1 == 0 and type_2 == 1:
        return 2

    return 'Error'

from PIL import Image, ImageDraw, ImageFont
def overlay(bkgd, id_image_1, id_image_2, nick_1, nick_2, poke_name_1, poke_name_2):
    background = Image.open(f'files_rps/image_pokemons/{bkgd}.png')
    img_1 = Image.open(f'files_rps/image_pokemons/{id_image_1}.png')
    img_2 = Image.open(f'files_rps/image_pokemons/{id_image_2}.png')

    background.paste(img_1, (100, 230),  img_1)
    background.paste(img_2, (1230, 230),  img_2)

    font = ImageFont.truetype("files_rps/image_pokemons/Pokemon.ttf", 100)
    drawer = ImageDraw.Draw(background)

    list_of_words = [[-50, 120, ' ' * ((21 - len(nick_1)) // 2) + nick_1], [1050, 120, ' ' * ((22 - len(nick_2)) // 2) + nick_2],
    [-50, 840, ' ' * ((21 - len(poke_name_1)) // 2) + poke_name_1], [1050, 840, ' ' * ((22 - len(poke_name_2)) // 2) + poke_name_2]]

    for x, y, text in list_of_words:
        offset = 7
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

        drawer.text((x, y), text, font=font, fill="#e8cc10")

    return background
