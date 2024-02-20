import pygame
from map import newMap

up_angle = pygame.Vector2(0,-1)
hitbox = pygame.Vector2(0,0.1)

class newPlayer():
    def __init__(self, pos, world : newMap) -> None:
        self.pos = pygame.Vector2(pos)
        self.world = world
        self.direction = up_angle
        self.angle = 145
        self.speed = 5
        self.turnspeed = 75

    def draw(self, surface, zoom = 1):
        pygame.draw.circle(surface, 'red', self.pos * zoom, 1)
        pygame.draw.line(surface, 'blue', self.pos, self.direction * 2 + self.pos)

    def Move(self, move):
        step_coords = self.pos + move
        if self.world.getCells(int(step_coords.x), int(step_coords.y)) == 0:
            self.pos = step_coords

    def input(self, dt) -> bool:
        quit = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            step = self.direction * dt * self.speed
            self.Move(step)
        elif keys[pygame.K_s]:
            step = self.direction * dt * self.speed
            self.Move(-step)
        if keys[pygame.K_q]:
            self.angle -= self.turnspeed * dt
        elif keys[pygame.K_d]:
            self.angle += self.turnspeed * dt
        if keys[pygame.K_ESCAPE]:
            quit = True

        self.angle = fix_angle(self.angle)
        self.direction = up_angle.rotate(self.angle)

        return quit
    
def fix_angle(angle) -> float:
    new_angle = angle
    while new_angle >= 360:
        new_angle -=360
    while new_angle < 0:
        new_angle +=360

    return new_angle
