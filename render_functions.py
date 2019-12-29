import tcod

def render_all(con, entities, game_map, screen_width, screen_height, colors):
    for y in range(game_map.height):
        for x in range(game_map.width):
            wall = game_map.tiles[x][y].block_sight

            if wall:
                # https://python-tcod.readthedocs.io/en/latest/libtcodpy.html#tcod.console_set_char_background
                tcod.console_set_char_background(con, x, y, colors.get('dark_wall'), tcod.BKGND_SET)
            else:
                tcod.console_set_char_background(con, x, y, colors.get('dark_ground'), tcod.BKGND_SET)
    
    for entity in entities:
        draw_entity(con, entity)
    
    # https://python-tcod.readthedocs.io/en/latest/libtcodpy.html#tcod.console_blit
    # Blit the console src from x,y,w,h to console dst at xdst,ydst
    #    console_blit(CON, x, y, w,            h,          DST, xdst, ydst)
    tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
    # This blits the entire console, in other words

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity):
    # https://python-tcod.readthedocs.io/en/latest/libtcodpy.html#tcod.console_set_default_foreground
    # Change the default foreground color for a console
    tcod.console_set_default_foreground(con, entity.color)
    # https://python-tcod.readthedocs.io/en/latest/libtcodpy.html#tcod.console_put_char
    # Draw the character c at x,y using the default colors and blend mode
    #    console_put_char(CON, x,        y,        c,           colors/blend)
    tcod.console_put_char(con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)

def clear_entity(con, entity):
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)
