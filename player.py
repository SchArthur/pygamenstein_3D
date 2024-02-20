import pygame

up_angle = pygame.Vector2(0,-1)

class newPlayer():
    def __init__(self, pos) -> None:
        self.pos = pygame.Vector2(pos)
        self.direction = up_angle
        self.angle = 145
        self.speed = 5
        self.turnspeed = 75

    def draw(self, surface, zoom = 1):
        pygame.draw.circle(surface, 'red', self.pos * zoom, 1)
        pygame.draw.line(surface, 'blue', self.pos, self.direction * 2 + self.pos)

    def input(self, dt) -> bool:
        quit = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            self.pos += self.direction * dt * self.speed
        elif keys[pygame.K_s]:
            self.pos -= self.direction * dt * self.speed
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
