import files_random_pvp.Pokemons_PvP as Pokemons_PvP
import random

def random_pvp(user_1, user_2):

    pokemon = Pokemons_PvP.list_pokemons[random.randint(0, len(Pokemons_PvP.list_pokemons) - 1)]

    items = [Pokemons_PvP.list_items[random.randint(0, len(Pokemons_PvP.list_items) - 1)]]
    while len(items) < 3:
        tmp = Pokemons_PvP.list_items[random.randint(0, len(Pokemons_PvP.list_items) - 1)]
        if tmp not in items:
            items.append(tmp)
    items = ', '.join(items)

    skill = Pokemons_PvP.list_skills[random.randint(0, len(Pokemons_PvP.list_skills) - 1)]

    msg = f'Пвп между капитанами {user_1} и {user_2}.\nПокемон: {pokemon}.\nПредметы: {items}.\nУмение: {skill}.'

    return msg
