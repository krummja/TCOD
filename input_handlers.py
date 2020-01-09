import tcod



def handle_keys(key):

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

    if key.char == 'g':
        return {'pickup': True}
    
    if key.vk == tcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    
    elif key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}
    
    return {}

