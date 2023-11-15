import pygame as pg

screen = pg.display.set_mode((500, 500))

potato_animation = pg.image.load('assets/images/turrets/potato_index.png').convert_alpha()


size = potato_animation.get_size()

print(size)

potato_sub = potato_animation.subsurface(0, 0, 45, 45)

game_running = True 

while game_running:
    
    for event in pg.event.get():
        # quit program
        if event.type == pg.QUIT:
            game_running = False

    pg.display.update()