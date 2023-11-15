import pygame as pg
import math

class Turret(pg.sprite.Sprite):
    
    def __init__(self, sprite_sheet, tile_x, tile_y) -> None:
        pg.sprite.Sprite.__init__(self)

        self.range = 99
        self.selected = False
        self.target = None

        self.tile_x = tile_x
        self.tile_y = tile_y
        # center coords
        self.x = (self.tile_x + 1) * 608/38 
        self.y = (self.tile_y + 1) * 400/25 
        # -----------------------------#
        #updating images
        self.sprite_sheet = sprite_sheet
        self.animation_index = self.load_images()
        self.frame = 0

        self.image = self.animation_index[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        #creating range circle
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)

    #finding the enemies
    def targetting(self, enemy_grp):
        x_dist = 0
        y_dist = 0
        #check range
        for enemy in enemy_grp:
            x_dist = enemy.pos[0] - self.x
            y_dist = enemy.pos[1] - self.y
            dist = math.sqrt(x_dist **2 + y_dist ** 2)
            if dist < self.range:
                self.target = enemy

    #pulling image frames for the animation
    def load_images(self):
        box = self.sprite_sheet.get_height()
        animation_list = []
        for i in range(8):
            img = self.sprite_sheet.subsurface(x * box, 0, box, box)
            animation_list.append(img)
        return animation_list