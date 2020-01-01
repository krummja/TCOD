import sys
import tcod

from entity import Entity
from fov_functions import initialize_fov, recompute_fov
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all


def main():
    #* Screen Variables
    screen_width = 80
    screen_height = 50

    #* Map Variables
    map_width = 80
    map_height = 45
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    colors = {
        'dark_wall': tcod.Color(0, 0, 100),
        'dark_ground': tcod.Color(50, 50, 150),
        'light_wall': tcod.Color(130, 110, 50),
        'light_ground': tcod.Color(200, 180, 50)
    }

    #* Entity Variables
    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', tcod.white)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', tcod.yellow)
    entities = [npc, player]

    #* Console Variables
    tcod.console_set_custom_font('./assets/arial10x10.png', tcod.FONT_TYPE_GRAYSCALE | tcod.FONT_LAYOUT_TCOD)
    tcod.console_init_root(screen_width, screen_height, 'tcod tutorial', False)
    con = tcod.console_new(screen_width, screen_height)

    #* Map Object Variables
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player)

    fov_recompute = True

    fov_map = initialize_fov(game_map)

    #* Control Variables
    key = tcod.Key()
    mouse = tcod.Mouse()

    #* Main Game Loop
    while not tcod.console_is_window_closed():
        curr_fps = tcod.sys_get_fps()
        for x in range(10):
            print('   FPS: ' + str(curr_fps), end='\r')

        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)
        
        #* Drawing Functions
        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)
        fov_recompute = False
        tcod.console_flush()
        clear_all(con, entities)
        
        #* Input Functions
        action = handle_keys(key)

        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        move = action.get('move')

        #* Control Logic
        #* Client 
        if exit:
            return True
        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        #* Game Controls
        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)

                fov_recompute = True


if __name__ == '__main__':
    main()

