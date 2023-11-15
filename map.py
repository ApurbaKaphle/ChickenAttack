import pygame as pg
import json

class Map():
    
    def __init__(self, data, map_image) -> None:
        self.waypoints = []
        self.placeables = []
        self.image = map_image
        self.level_data = data

        with open('levels/TD_Game/simplified/Level_1/data.json') as file:
            self.player_stats = json.load(file)
        self.health = json.load('stats.json')

    

    def process_data(self):
        # extract relevant info from map file

        waypoint_data = self.level_data['entities']['Line'][0]['customFields']['Point']
        
        for point in waypoint_data:

            # grid contains 608 pix / 38 cells in x and 400 pix / 25 cells in y
            x_coord = point.get('cx') * 608/38
            y_coord = point.get('cy') * 400/25
            
            self.waypoints.append((x_coord, y_coord))

        placeable_data = self.level_data['entities']['Turret_Placings']
        for points in placeable_data:
            xcoord = points['x']
            ycoord = points['y']

            self.placeables.append((xcoord, ycoord))

    def place_check(self, mouse_pos):
        # method to make sure selected tower is being placed inside one of the placeable regions
        
        for pts in self.placeables:
            x, xmax, xmin = mouse_pos[0], pts[0] + 32, pts[0]
            y, ymax, ymin = mouse_pos[1], pts[1] + 32, pts[1]

            if xmin <= x <= xmax and ymin <= y <= ymax:
                return pts

        return False


    def draw(self, surface):
        surface.blit(self.image, (0,0))
