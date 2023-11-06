import pygame as pg
import math

class Turret(pg.sprite.Sprite):
    
    def __init__(self, image, tile_x, tile_y) -> None:
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
        self.image = image
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