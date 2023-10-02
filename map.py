import pygame as pg
import json

class Map():
    
    def __init__(self, data, map_image) -> None:
        self.waypoints = []
        self.image = map_image
        self.level_data = data
    

    def process_data(self):
        # extract relevant info from map file

        waypoint_data = self.level_data['entities']['Line'][0]['customFields']['Point']
        
        for point in waypoint_data:

            # grid contains 608 pix / 38 cells in x and 400 pix / 25 cells in y
            x_coord = point.get('cx') * 608/38
            y_coord = point.get('cy') * 400/25

            self.waypoints.append((x_coord, y_coord))
            
    def draw(self, surface):
        surface.blit(self.image, (0,0))
