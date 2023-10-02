import pygame as pg
from pygame.math import Vector2

class Enemy(pg.sprite.Sprite):

    def __init__(self, waypoints, image) -> None:
        
        pg.sprite.Sprite.__init__(self)

        # location information
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1

        # image information
        self.angle = 0
        self.orig_image = image
        self.image = pg.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect()   
        self.rect.center = self.pos

        # stats
        self.speed = 0.5

    def update(self):
        self.move()
        self.rotate()


    def move(self):
        # target waypoint

        if self.target_waypoint < len(self.waypoints):
            # enemy is on the path

            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        
        else:
            # enemy is at the end of the path
            self.kill()

        dist = self.movement.length()
        # check if distance left is more than enemy speed
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed

        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1
    
    def rotate(self):

        # calc distance to next waypoint

        dist = self.target - self.pos
        
        self.angle = dist.angle_to((dist[0], 0))

        self.image = pg.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect()   
        self.rect.center = self.pos