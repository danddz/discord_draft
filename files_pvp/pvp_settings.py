count_ban = 0 * 2
count_pick = 1 * 2

ban_pick = [
    [0, 1, -1]
]


from PIL import Image, ImageDraw, ImageFont

def overlay(bkgd, id_image_1, id_image_2, id_image_3, nick_1, nick_2, poke_name_1, poke_name_2, poke_name_3):
    background = Image.open(f'files_pvp/image_pokemons/{bkgd}.png')
    img_1 = Image.open(f'files_pvp/image_pokemons/{id_image_1}.png')
    img_2 = Image.open(f'files_pvp/image_pokemons/{id_image_2}.png')
    img_3 = Image.open(f'files_pvp/image_pokemons/{id_image_3}.png')

    background.paste(img_1, (65, 300),  img_1)
    background.paste(img_2, (710, 300),  img_2)
    background.paste(img_3, (1365, 300),  img_3)

    font = ImageFont.truetype("files_pvp/image_pokemons/Pokemon.ttf", 100)
    drawer = ImageDraw.Draw(background)

    list_of_words = [[-50, 90, ' ' * ((21 - len(nick_1)) // 2) + nick_1], [1000, 90, ' ' * ((22 - len(nick_2)) // 2) + nick_2],
    [-140, 800, ' ' * ((21 - len(poke_name_1)) // 2) + poke_name_1], [460, 800, ' ' * ((22 - len(poke_name_2)) // 2) + poke_name_2],
    [1110, 800, ' ' * ((22 - len(poke_name_3)) // 2) + poke_name_3]]

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
