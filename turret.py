import pygame as pg
import math
import json

class Turret(pg.sprite.Sprite):
    
    def __init__(self, name, sprite_sheet, tile_x, tile_y) -> None:
        pg.sprite.Sprite.__init__(self)

        self.last_shot = pg.time.get_ticks()
        
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
        self.update_time = pg.time.get_ticks()

        self.angle = 90
        self.og_image = self.animation_index[self.frame]
        self.image = pg.transform.rotate(self.og_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # turret stats
        self.stats = json.load(open('stats.json'))['turrets'][name]
        self.attack = self.stats['attack']
        self.range = self.stats['range']
        self.cooldown = self.stats['cooldown']
        self.cost = self.stats['cost']

        #creating range circle
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def draw(self, surface):
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.image = pg.transform.rotate(self.og_image, self.angle - 90)
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)

    #finding the enemies
    def targeting(self, enemy_grp):
        x_dist = 0
        y_dist = 0
        #check range
        for enemy in enemy_grp:
            x_dist = enemy.pos[0] - self.x
            y_dist = enemy.pos[1] - self.y
            dist = math.sqrt(x_dist **2 + y_dist ** 2)
            if dist < self.range:
                self.target = enemy
                self.amgle = math.degrees(math.atan2(-y_dist, x_dist))

                self.target.health -= self.attack
                break

    #pulling image frames for the animation
    def load_images(self):
        box = self.sprite_sheet.get_height()
        animation_list = []
        for i in range(8):
            img = self.sprite_sheet.subsurface(i*box, 0, box, box)
            animation_list.append(img)
        return animation_list
    
    #updating the loaded image
    def play_animation(self):
        self.og_image = self.animation_index[self.frame]
        if pg.time.get_ticks() - self.update_time > 99:
            self.update_time = pg.time.get_ticks()
            self.frame += 1
            if self.frame >= len(self.animation_index):
                self.frame = 0
                self.last_shot = pg.time.get_ticks()
                self.target = None

    def update(self, enemy_grp):
        if self.target:
            self.play_animation()
        else:
            if pg.time.get_ticks() - self.last_shot > self.cooldown:
                self.targeting(enemy_grp)
