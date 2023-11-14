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
selected_chicken = None
paused = False

#-------------------------------------------------------images-------------------------------------------------------#
# map
pause_screen = pg.transform.scale_by(pg.image.load('levels/TD_Game/simplified/Level_0/Tiles.png').convert_alpha(), 0.5)
level1 = pg.image.load('levels/TD_Game/simplified/Level_1/Tiles.png').convert_alpha()
# turret
chicken_turret = pg.transform.scale_by(pg.image.load('assets/images/turrets/chicken1_edited.png'), 0.25)
potato_turret = pg.transform.scale_by(pg.image.load('assets/images/turrets/potato_turret.png'), 0.075)
# enemies
enemy_image = pg.transform.scale_by(pg.image.load('assets/images/enemies/enemy_2.png').convert_alpha(), 0.15)
# shop buttons
buy_chicken_turret_image = pg.transform.scale_by(pg.image.load('assets/images/turrets/chicken1.png'), 0.3)
buy_potato_turret_image = pg.transform.scale_by(pg.image.load('assets/images/turrets/potato_turret.png'), 0.2)
cancel_image = pg.transform.scale_by(pg.image.load('assets/images/buttons/red_x.png'), 0.1)
# general buttons
menu_button_image = pg.transform.scale_by(pg.image.load('assets/images/buttons/menu_button.png'), 0.25)

#-------------------------------------------------------Map-------------------------------------------------------#

with open('levels/TD_Game/simplified/Level_1/data.json') as file:
    data = json.load(file)

def pause_check():
    game_screen.blit(pause_screen, (0,0))
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        
        if menu_button.draw(game_screen):
            break

        pg.display.update()
        clock.tick(15)

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
           
def select_chicken(mouse_pos):
    mouse_tile_x = mouse_pos[0] // xTileSize
    mouse_tile_y = mouse_pos[1] // yTileSize
    for turret in turret_grp:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret
        
def clear_selection():
    for turret in turret_grp:
        turret.selected = False

map = Map(data, level1)
map.process_data()

# groups
enemy_grp = pg.sprite.Group()
turret_grp = pg.sprite.Group()

enemy = Enemy(map.waypoints, enemy_image)

enemy_grp.add(enemy)

#adding buttons
chicken_turret_button = Button(WINDOW_WIDTH + 40, 50, buy_chicken_turret_image, True)
potato_turret_button = Button(WINDOW_WIDTH + 150, 50, buy_potato_turret_image, True)
cancel_button = Button(WINDOW_WIDTH + 60, 100, cancel_image, True)
menu_button = Button(WINDOW_WIDTH - 130, 10, menu_button_image, True)
# game loop
game_running = True

while game_running:
    clock.tick(FPS)

    game_screen.fill('#696969')

    map.draw(game_screen)
    #selecting chicken
    if selected_chicken:
        selected_chicken.selected = True
    
    # adding points where turrets can be placed
    for pt in map.placeables:
        rects = pg.Rect(pt, (32, 32))
        pg.draw.rect(game_screen, 'red', rects, 2)
    # update grps
    enemy_grp.update()

    # draw grps
    enemy_grp.draw(game_screen)
    for turret in turret_grp:
        turret.draw(game_screen)
    
    # draw buttons
    if chicken_turret_button.draw(game_screen):
        placing_turrets = True
        cursor_turret = chicken_turret

    if potato_turret_button.draw(game_screen):
        placing_turrets = True
        cursor_turret = potato_turret
<<<<<<< HEAD
=======
    
    if menu_button.draw(game_screen):
        pause_check()     
>>>>>>> 7fe08af64cf97bf22ca60abb8caa62de7a216f53

    if placing_turrets:
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
            
            if mouse_pos[0] < WINDOW_WIDTH and mouse_pos[1] < WINDOW_HEIGHT:
                check = map.place_check(mouse_pos)
                selected_chicken = None
                clear_selection()
                if placing_turrets and check:
                    create_turret(check)
                
                elif not placing_turrets and check:
                    selected_chicken = select_chicken(check)

    pg.display.update()


pg.quit()
