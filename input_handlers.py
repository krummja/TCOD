import tcod

from game_states import GameStates


def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state == GameStates.TARGETING:
        return handle_player_dead_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)

    return {}


def handle_player_turn_keys(key):
    key_char = chr(key.c)

    if key.vk == tcod.KEY_KP8:
        return {'move': (0, -1)}
    elif key.vk == tcod.KEY_KP2:
        return {'move': (0, 1)}
    elif key.vk == tcod.KEY_KP4:
        return {'move': (-1, 0)}
    elif key.vk == tcod.KEY_KP6:
        return {'move': (1, 0)}
    elif key.vk == tcod.KEY_KP7:
        return {'move': (-1, -1)}
    elif key.vk == tcod.KEY_KP9:
        return {'move': (1, -1)}
    elif key.vk == tcod.KEY_KP1:
        return {'move': (-1, 1)}
    elif key.vk == tcod.KEY_KP3:
        return {'move': (1, 1)}

    if key_char == 'd':
        return {'drop_inventory': True}

    if key_char == 'g':
        return {'pickup': True}

    elif key_char == 'i':
        return {'show_inventory': True}
    
    if key.vk == tcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    
    elif key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}
    
    return {}


def handle_targeting_keys(key):
    if key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}
    
    return {}


def handle_player_dead_keys(key):
    key_char = chr(key.c)

    if key_char == 'i':
        return {'show_inventory': True}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    
    elif key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}
    
    return {}


def handle_inventory_keys(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'inventory_index': index}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    elif key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}
    
    return {}


def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}
    
    return {}