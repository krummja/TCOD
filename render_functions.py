import tcod

from enum import Enum, auto

from game_states import GameStates
from menus import inventory_menu


class RenderOrder(Enum):
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()


def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
            if entity.x == x and entity.y == y and tcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()


def targeting_area(mouse, game_state, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    if tcod.map_is_in_fov(fov_map, x, y) and game_state == GameStates.TARGETING:
        tcod.console_set_default_foreground(con, tcod.orange)
        tcod.console_put_char(con, x, y, '*', tcod.BKGND_NONE)


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    tcod.console_set_default_background(panel, back_color)
    tcod.console_rect(panel, x, y, total_width, 1, False, tcod.BKGND_SCREEN)

    tcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        tcod.console_rect(panel, x, y, bar_width, 1, False, tcod.BKGND_SCREEN)

    tcod.console_set_default_foreground(panel, tcod.white)
    tcod.console_print_ex(panel, int(x + total_width / 2), y, tcod.BKGND_NONE, tcod.CENTER,
                             '{0}: {1}/{2}'.format(name, value, maximum))


def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, bar_width, panel_height, panel_y, mouse, colors, game_state):
    
    # Render Game Map
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = tcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        tcod.console_put_char(con, x, y, '#', tcod.BKGND_NONE)
                        tcod.console_set_char_foreground(con, x, y, colors.get('light_wall'))
                    else:
                        tcod.console_put_char(con, x, y, '.', tcod.BKGND_NONE)
                        tcod.console_set_char_foreground(con, x, y, colors.get('light_ground'))
                    
                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    if wall:
                        tcod.console_put_char(con, x, y, '#', tcod.BKGND_NONE)
                        tcod.console_set_char_foreground(con, x, y, colors.get('dark_wall'))
                    else:
                        tcod.console_put_char(con, x, y, '.', tcod.BKGND_NONE)
                        tcod.console_set_char_foreground(con, x, y, colors.get('dark_ground'))
    
    # Render Entities
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map)

    # Render GUI
    tcod.console_set_default_foreground(con, tcod.white)
    tcod.console_print_ex(con, 1, screen_height - 2, tcod.BKGND_NONE, tcod.LEFT,
    'HP: {0:02}/{1:02}'.format(player.fighter.hp, player.fighter.max_hp))

    tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    tcod.console_set_default_background(panel, tcod.black)
    tcod.console_clear(panel)

    # Print game messages one line at a time
    y = 1
    for message in message_log.messages:
        tcod.console_set_default_foreground(panel, message.color)
        tcod.console_print_ex(panel, message_log.x, y, tcod.BKGND_NONE, tcod.LEFT, message.text)
        y += 1

    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp, tcod.light_red, tcod.darker_red)

    tcod.console_set_default_foreground(panel, tcod.light_grey)
    tcod.console_print_ex(panel, 1, 0, tcod.BKGND_NONE, tcod.LEFT, get_names_under_mouse(mouse, entities, fov_map))

    tcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)

    # Inventory state
    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
        else:
            inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'
        
        inventory_menu(con, inventory_title, player.inventory, 50, screen_width, screen_height)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map):
    if tcod.map_is_in_fov(fov_map, entity.x, entity.y):
        tcod.console_set_default_foreground(con, entity.color)
        tcod.console_put_char(con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)
    

def clear_entity(con, entity):
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)
