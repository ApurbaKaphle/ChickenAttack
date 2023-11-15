import pygame as pg
import json
from enemies import Enemy
from map import Map
from turret import Turret
from button import Button
#hi WE WIN!!!
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
last_enemy_spawn = pg.time.get_ticks()
start = False
game_over = False
game_outcome = 0

#-------------------------------------------------------images-------------------------------------------------------#
# map
level1 = pg.image.load('levels/TD_Game/simplified/Level_1/Tiles.png').convert_alpha()
# turret
chicken_turret = pg.transform.scale_by(pg.image.load('assets/images/turrets/chicken1_edited.png'), 0.25)
potato_turret = pg.transform.scale_by(pg.image.load('assets/images/turrets/potato_turret.png'), 0.075)
potato_animation = pg.transform.scale_by(pg.image.load('assets/images/turrets/potato_index.png'), 0.075)
chicken_animation = pg.transform.scale_by(pg.image.load('assets/images/turrets/chicken_index.png'), 0.075)
# enemies
enemy_images = {
    "final_boss": pg.transform.scale_by(pg.image.load('assets/images/enemies/enemy_2.png').convert_alpha(), 0.15),
    "enemy3": pg.transform.scale_by(pg.image.load('assets/images/enemies/enemy_3.png').convert_alpha(), 0.04)
}

# shop buttons
buy_chicken_turret_image = pg.transform.scale_by(pg.image.load('assets/images/turrets/chicken1.png'), 0.3)
buy_potato_turret_image = pg.transform.scale_by(pg.image.load('assets/images/turrets/potato_turret.png'), 0.2)
cancel_image = pg.transform.scale_by(pg.image.load('assets/images/buttons/red_x.png'), 0.1)
# general buttons
menu_button_image = pg.transform.scale_by(pg.image.load('assets/images/buttons/menu_button.png'), 0.25)
store_button_image = pg.transform.scale_by(pg.image.load('levels/TD_Game/simplified/Store_Button/Tiles.png').convert_alpha(), 0.75)
start_button_image = pg.transform.scale_by(pg.image.load('levels/TD_Game/simplified/Start_Button/Tiles.png'), 1)
new_game_image = pg.transform.scale_by(pg.image.load('levels/TD_Game/simplified/NewGame_Button/Tiles.png'), 0.3)

pause_screen = pg.transform.scale_by(pg.image.load('assets/images/buttons/pause_screen.png').convert_alpha(), 0.5)
pause_width, pause_height = pause_screen.get_size()
menu_cont_image = pause_screen.subsurface(0, 0, pause_width, pause_height/3)
menu_settings_image = pause_screen.subsurface(0, pause_height/3, pause_width, pause_height/3)
menu_quit_image = pause_screen.subsurface(0, 2*pause_height/3, pause_width, pause_height/3)

background_fx = pg.mixer.Sound('assets/audio/background.wav')
background_fx.set_volume(0.01)

#-------------------------------------------------------Functions-------------------------------------------------------#
with open('levels/TD_Game/simplified/Level_1/data.json') as file:
    data = json.load(file)

# fonts
text_font = pg.font.SysFont("Consolas", 24, bold = True)
large_font = pg.font.SysFont("Consolas", 36)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)

    game_screen.blit(img, (x,y))

def pause_check():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        
        if menu_quit_button.draw(game_screen):
            pg.quit()
            quit()

        if (menu_button.draw(game_screen) or menu_cont_button.draw(game_screen)):
            break
        
        elif menu_settings_button.draw(game_screen):
            print('test')

        pg.display.update()
        clock.tick(15)

def create_turret(mouse_pos, name, cursor_animation):

    mouse_tile_x = mouse_pos[0] // xTileSize
    mouse_tile_y = mouse_pos[1] // yTileSize

    space_is_free = True
    for turret in turret_grp:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            space_is_free = False
    
    if space_is_free == True:      
        new_turret = Turret(name, cursor_animation, mouse_tile_x, mouse_tile_y)
        if map.money >= new_turret.cost:
            turret_grp.add(new_turret)

            # give me your money
            map.money -= new_turret.cost
           
def select_chicken(mouse_pos):
    mouse_tile_x = mouse_pos[0] // xTileSize
    mouse_tile_y = mouse_pos[1] // yTileSize
    for turret in turret_grp:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret
        
def clear_selection():
    for turret in turret_grp:
        turret.selected = False

#-------------------------------------------------------Map-------------------------------------------------------#
map = Map(data, level1)
map.process_data()
map.process_enemies()

# groups
enemy_grp = pg.sprite.Group()
turret_grp = pg.sprite.Group()


#-------------------------------------------------------Buttons-------------------------------------------------------#

# turrets
store_button = Button(WINDOW_WIDTH + shop/4, 10, store_button_image, True)
chicken_turret_button = Button(store_button.rect.midbottom[0] - 100, store_button.rect.midbottom[1] + 50, buy_chicken_turret_image, True)
potato_turret_button = Button(store_button.rect.midbottom[0] + 15, store_button.rect.midbottom[1] + 50, buy_potato_turret_image, True)
cancel_button = Button(WINDOW_WIDTH + 60, 100, cancel_image, True)
start_button = Button(WINDOW_WIDTH + 60, 300, start_button_image, True)
new_game_button = Button(WINDOW_WIDTH + 60, 300, new_game_image, True)

menu_button = Button(WINDOW_WIDTH - 130, 10, menu_button_image, True)
menu_cont_button = Button(WINDOW_WIDTH/2 - 175, 40, menu_cont_image, True)
menu_settings_button = Button(WINDOW_WIDTH/2 - 175, 45 + pause_height/3, menu_settings_image, True)
menu_quit_button = Button(WINDOW_WIDTH/2 - 175, 50 + 2*pause_height/3, menu_quit_image, True)

#-------------------------------------------------------Game Loop-------------------------------------------------------#
game_running = True
background_fx.play()
while game_running:
    clock.tick(FPS)

    game_screen.fill("#c77d0e")

    map.draw(game_screen)

    # adding points where turrets can be placed
    for pt in map.placeables:
        rects = pg.Rect(pt, (32, 32))
        pg.draw.rect(game_screen, 'red', rects, 2)

    # updating game over to 1/0
    if game_over == False:
        if map.health <= 0:
            game_over = True
            game_outcome = -1
        if map.tot_kill == len(map.enemy_list):
            game_over == True
            game_outcome = 1
        # update grps
        enemy_grp.update(map)
        turret_grp.update(enemy_grp)

        #selecting chicken
        if selected_chicken:
            selected_chicken.selected = True

    # draw grps
    enemy_grp.draw(game_screen)
    
    for turret in turret_grp:
        turret.draw(game_screen)

    draw_text(str(map.health), text_font, 'red', 0, 0)
    draw_text(str(map.money), large_font, 'yellow', store_button.rect.midbottom[0], store_button.rect.midbottom[1])

    store_button.draw(game_screen)

    #checks to see if you failed
    if game_over == True and game_outcome == -1:
        print("test2")
        draw_text("You Lose Noob... GET GUD", large_font, 'black', 100, (WINDOW_HEIGHT/2))
        if new_game_button.draw(game_screen):
            #reseting game
            game_over = False
            game_outcome = 0
            map.health = 100
            start = False
            placing_turrets = False
            selected_chicken = None
            last_enemy_spawn = pg.time.get_ticks()
            map = Map(data, level1)
            map.process_data()
            map.process_enemies()
            enemy_grp.empty()
            turret_grp.empty()

    if game_over == True and game_outcome == 1:
        draw_text("You're the BEST", large_font, 'black', 100, (WINDOW_HEIGHT/2))

    if game_over == False:
        #time before game//start
        if start == False:
            if start_button.draw(game_screen):
                start = True
        else:
            #enemy spawns
            if pg.time.get_ticks() - last_enemy_spawn > 1000:
                if map.spawned_enemies < len(map.enemy_list):
                    enemy_type = map.enemy_list[map.spawned_enemies]
                    enemy = Enemy(enemy_type, map.waypoints, enemy_images)
                    enemy_grp.add(enemy)
                    map.spawned_enemies += 1
                    last_enemy_spawn = pg.time.get_ticks()
        
        # draw buttons
        if chicken_turret_button.draw(game_screen):
            placing_turrets = True
            cursor_turret = chicken_turret
            cursor_turret_name = 'chicken_turret'
            cursor_animation = chicken_animation

        if potato_turret_button.draw(game_screen):
            placing_turrets = True
            cursor_turret = potato_turret
            cursor_turret_name = 'potato_turret'
            cursor_animation = potato_animation
        
        if menu_button.draw(game_screen):
            pause_check()

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
                    # checks to see if you're broke or not
                    create_turret(check, cursor_turret_name, cursor_animation)
                
                elif not placing_turrets and check:
                    selected_chicken = select_chicken(check)

    pg.display.update()


pg.quit()
