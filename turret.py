import pygame as pg

class Turret(pg.sprite.Sprite):
    
    def __init__(self, image, tile_x, tile_y) -> None:
        pg.sprite.Sprite.__init__(self)
        self.tile_x = tile_x
        self.tile_y = tile_y
        # center coords
        self.x = (self.tile_x + 0.5) * 608/38 
        self.y = (self.tile_y + 0.5) * 400/25
        # -----------------------------#
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)