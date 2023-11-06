import pygame as pg
import json
from enemies import Enemy
from map import Map
from turret import Turret
from button import Button

#-------------------------------------------------------constants-------------------------------------------------------#
xRows = 38
yCols = 25
xTileSize = 608/38
yTileSize = 400/25
shop = 300
WINDOW_WIDTH = xTileSize * xRows
WINDOW_HEIGHT = yTileSize * yCols
FPS = 60

#-------------------------------------------------------initialize pygame-------------------------------------------------------#
pg.init()
game_screen = pg.display.set_mode((WINDOW_WIDTH + shop, WINDOW_HEIGHT))
clock = pg.time.Clock()

pg.display.set_caption('Chicken Attack!')

#------------------------------------------------------Game Variables-----------------------------------------------------#
placing_turrets = False

#-------------------------------------------------------images-------------------------------------------------------#
# map
map_image = pg.image.load('levels/level0/simplified/Level_0/tiles.png').convert_alpha()
# turret
cursor_turret = pg.transform.scale_by(pg.image.load('assets/images/turrets/chicken1.png'), 0.15)
# enemies
enemy_image = pg.transform.scale_by(pg.image.load('assets/images/enemies/enemy_2.png').convert_alpha(), 0.15)
# shop buttons
buy_turret_image = pg.transform.scale_by(pg.image.load('assets/images/turrets/chicken1.png'), 0.3)
cancel_image = pg.transform.scale_by(pg.image.load('assets/images/buttons/red_x.png'), 0.1)

#-------------------------------------------------------Map-------------------------------------------------------#

with open('levels/level0/simplified/Level_0/data.json') as file:
    data = json.load(file)

def create_turret(mouse_pos):

    mouse_tile_x = mouse_pos[0] // xTileSize
    mouse_tile_y = mouse_pos[1] // yTileSize

    space_is_free = True
    for turret in turret_grp:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            space_is_free = False
    if space_is_free == True:      
        new_turret = Turret(cursor_turret, mouse_tile_x, mouse_tile_y)
        turret_grp.add(new_turret)


map = Map(data, map_image)
map.process_data()

# groups
enemy_grp = pg.sprite.Group()
turret_grp = pg.sprite.Group()

enemy = Enemy(map.waypoints, enemy_image)

enemy_grp.add(enemy)

#adding buttons
turret_button = Button(WINDOW_WIDTH + 100, 120, buy_turret_image)
cancel_button = Button(WINDOW_WIDTH + 60, 100, cancel_image)

# game loop
game_running = True

while game_running:
    clock.tick(FPS)

    game_screen.fill('#696969')

    map.draw(game_screen)
    
    # adding points where turrets can be placed
    for pt in map.placeables:
        rects = pg.Rect(pt, (32, 32))
        pg.draw.rect(game_screen, 'red', rects, 2)
    # update grps
    enemy_grp.update()

    # draw grps
    enemy_grp.draw(game_screen)
    turret_grp.draw(game_screen)
    
    # draw buttons
    if turret_button.draw(game_screen):
        placing_turrets = True

    if placing_turrets ==True:
        cursor_rect = cursor_turret.get_rect()
        cursor_pos = pg.mouse.get_pos()
        cursor_rect.center = cursor_pos
        if cursor_pos[0] <= WINDOW_WIDTH:
            game_screen.blit(cursor_turret, cursor_rect)

        if cancel_button.draw(game_screen):
            placing_turrets = False


    for event in pg.event.get():

        # quit program
        if event.type == pg.QUIT:
            game_running = False

        # mouse click
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()

            # check if mouse is in allowed area
            
            if mouse_pos[0] < WINDOW_WIDTH and mouse_pos[1] < WINDOW_HEIGHT and (mouse_pos[0], mouse_pos[1]) in map.placeables:
                if placing_turrets == True:
                    create_turret(mouse_pos)
        

    pg.display.update()


pg.quit()
