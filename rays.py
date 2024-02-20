import pygame
import math
import map
import textureLoader

class newRay():
    def __init__(self, pos : pygame.Vector2, angle, map : map.newMap) -> None:
        in_cell_x = pos.x % 1
        in_cell_y = pos.y % 1
        position_in_cell = pygame.Vector2(in_cell_x,in_cell_y)

        # COORDINATES
        if angle == 0 or angle == 180 :
            # JOUEUR VERTICAL
            self.hit_type = 'hor'
            h = 0
            ray = self.hor_check(position_in_cell, angle, h) + pos
            while not map.hasHitWall(ray)[0]:
                h += 1
                ray = self.hor_check(position_in_cell, angle, h) + pos
        elif angle == 90 or angle == 270 :
            # JOUEUR HORIZONTAL
            self.hit_type = 'ver'
            v = 0
            ray = self.ver_check(position_in_cell, angle, v) + pos
            while not map.hasHitWall(ray)[0]:
                v += 1
                ray = self.ver_check(position_in_cell, angle, v) + pos
        else:
            # ENTRE 2
            v = 0
            v_distance = self.ver_check(position_in_cell, angle, v)
            ray_v = v_distance + pos
            while not map.hasHitWall(ray_v)[0]:
                v += 1
                v_distance = self.ver_check(position_in_cell, angle, v)
                ray_v = v_distance + pos

            h = 0
            h_distance = self.hor_check(position_in_cell, angle, h)
            ray_h = h_distance + pos
            while not map.hasHitWall(ray_h)[0]:
                h += 1
                h_distance = self.hor_check(position_in_cell, angle, h)
                ray_h = h_distance + pos

            if v_distance.length() < h_distance.length() :
                ray = ray_v
                self.hit_type = 'ver'
            else :
                ray = ray_h
                self.hit_type = 'hor'

        self.texture_type = map.hasHitWall(ray)[1] -1
        self.hit_ray_coords = ray

        if self.hit_type == 'ver':
            self.texture_coord = self.hit_ray_coords[1] % 1
        elif self.hit_type == 'hor':
            self.texture_coord = self.hit_ray_coords[0] % 1

    def getTexture(self, texture : textureLoader.wallTexture) -> pygame.surface.Surface:
        texture = texture.getStripe(self.texture_coord, self.texture_type, self.hit_type)
        return texture

    def hor_check(self, pos_in_cell : pygame.Vector2, angle, steps = 0):
        # renvoi la coordonnées de la 'steps' ème line horizontale que croise le joueur à l'angle 'angle'
        calc_angle = rotateAngle(angle, -90)
        if calc_angle != 90 and calc_angle != 270:
            if calc_angle < 180 :
                # DOWN
                y_nearest = 1 - pos_in_cell.y
                y_step = 1
            else :
                # UP
                y_nearest = -pos_in_cell.y
                y_step = -1
            x_nearest = y_nearest / math.tan(calc_angle * math.pi/180)
            x_step = y_step / math.tan(calc_angle * math.pi/180)
        elif calc_angle == 90:
            # PILE EN BAS
            x_nearest = pos_in_cell.x
            y_nearest = 1
            x_step = 0
            y_step = 1
        elif calc_angle == 270:
            # PILE EN HAUT
            x_nearest = pos_in_cell.x
            y_nearest = 0
            x_step = 0
            y_step = -1
        
        nearest_point = pygame.Vector2(x_nearest, y_nearest)
        point = nearest_point
        for i in range(steps):
            point += pygame.Vector2(x_step, y_step)

        return point

    def ver_check(self, pos_in_cell : pygame.Vector2, angle, steps = 0):
        # renvoi la coordonnées de la 'steps' ème line verticale que croise le joueur à l'angle 'angle'
        calc_angle = rotateAngle(angle, -90)
        if calc_angle != 0 and calc_angle !=180:
            if angle < 180 :
                # DROITE
                x_nearest = 1 - pos_in_cell.x
                x_step = 1
            else :
                # GAUCHE
                x_nearest = -pos_in_cell.x
                x_step = -1
            y_nearest = x_nearest * math.tan(calc_angle * math.pi/180)
            y_step = x_step * math.tan(calc_angle * math.pi/180)          
        elif calc_angle == 0:
            # PILE A DROITE
            x_nearest = 1
            y_nearest = pos_in_cell.y
            x_step = 1
            y_step = 0
        elif calc_angle == 180:
            #PILE A GAUCHE
            x_nearest = 0
            y_nearest = pos_in_cell.y
            x_step = -1
            y_step = 0

        nearest_point = pygame.Vector2(x_nearest, y_nearest)
        point = nearest_point
        for i in range(steps):
            point += pygame.Vector2(x_step, y_step)

        return point
    

def rotateAngle(angle, rotation):
    new_angle = angle
    new_angle += rotation
    while new_angle >= 360:
        new_angle -=360
    while new_angle < 0:
        new_angle +=360

    return new_angle

# test = newRay(pygame.Vector2(2.43,5.43244), 0, map.newMap('map_1.ini'))
# print(test.hit_ray_coords)