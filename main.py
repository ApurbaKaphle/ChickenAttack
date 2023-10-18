import pygame as pg
import json
from enemies import Enemy
from map import Map
from turret import Turret

# testing commits

#-------------------------------------------------------constants-------------------------------------------------------#
xRows = 38
yCols = 25
xTileSize = 608/38
yTileSize = 400/25
WINDOW_WIDTH = xTileSize * xRows
WINDOW_HEIGHT = yTileSize * yCols
FPS = 60

#-------------------------------------------------------initialize pygame-------------------------------------------------------#
pg.init()
game_screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pg.time.Clock()

pg.display.set_caption('TD Game')

#-------------------------------------------------------images-------------------------------------------------------#
# map
map_image = pg.image.load('levels/level0/simplified/Level_0/tiles.png').convert_alpha()
# turret
cursor_turret = pg.transform.scale_by(pg.image.load('assets/images/turrets/chicken1.png'), 0.1)
# enemies
enemy_image = pg.transform.scale_by(pg.image.load('assets/images/enemies/enemy_2.png').convert_alpha(), 0.15)

#-------------------------------------------------------Map-------------------------------------------------------#

with open('levels/level0/simplified/Level_0/data.json') as file:
    data = json.load(file)

def create_turret(mouse_pos):

    mouse_tile_x = mouse_pos[0] // xTileSize
    mouse_tile_y = mouse_pos[1] // yTileSize

    turret = Turret(cursor_turret, mouse_tile_x, mouse_tile_y)
    turret_grp.add(turret)


map = Map(data, map_image)
map.process_data()

# groups
enemy_grp = pg.sprite.Group()
turret_grp = pg.sprite.Group()

enemy = Enemy(map.waypoints, enemy_image)

enemy_grp.add(enemy)

# game loop
game_running = True



while game_running:
    clock.tick(FPS)

    game_screen.fill('#696969')

    map.draw(game_screen)
    
    # enemy path
    pg.draw.lines(game_screen, 'red', False, map.waypoints)
    # update grps
    enemy_grp.update()

    # draw grps
    enemy_grp.draw(game_screen)
    turret_grp.draw(game_screen)

    for event in pg.event.get():

        # quit program
        if event.type == pg.QUIT:
            game_running = False

        # mouse click
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()

            # check if mouse is in allowed area
            
            if mouse_pos[0] < WINDOW_WIDTH and mouse_pos[1] < WINDOW_HEIGHT:

                create_turret(mouse_pos)
        

    pg.display.update()


pg.quit()
