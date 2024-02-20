import pygame
import player
from map import newMap
from rays import newRay

# settings
minimap_zoom = 10
fov = 120
fullscreen = False

class game():
    def __init__(self) -> None:
        self.screen = pygame.surface.Surface((320,200))
        pygame.init()
        if not fullscreen:
            self.windows = pygame.display.set_mode((1280, 720))
        else:
            fullscreen_size = pygame.display.get_desktop_sizes()[0]
            self.windows = pygame.display.set_mode(fullscreen_size)
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.player = player.newPlayer((3,3))

        self.map = newMap('map_1.ini')

        self.run()

    def run(self):
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            self.running = not self.player.input(self.dt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # fill the screen with a color to wipe away anything from last frame
            top_rect = pygame.rect.Rect((0,0), (self.screen.get_width(),self.screen.get_height()/2))
            bot_rect = pygame.rect.Rect((0,self.screen.get_height()/2), (self.screen.get_width(),self.screen.get_height()/2))
            self.screen.fill("#909090", top_rect)
            self.screen.fill('#C0C0C0', bot_rect)

            self.screen = pygame.transform.scale(self.screen, (self.windows.get_width(), self.windows.get_height()))
            self.windows.blit(self.screen, (0,0))

            minimap = self.map.getMiniMap()
            minimap = pygame.transform.scale(minimap, (self.map.map_width * minimap_zoom, self.map.map_height * minimap_zoom))

            ray_delta = fov/self.screen.get_width()
            pixel_per_row = self.screen.get_width()
            for i in range(pixel_per_row):
                hit_coords = newRay(self.player.pos, player.fix_angle(self.player.angle + (i*ray_delta)-(fov/2)), self.map).hit_ray_coords
                pygame.draw.line(minimap, 'pink', self.player.pos * minimap_zoom, hit_coords * minimap_zoom)
                # distance_hit = hit[0]
                # ratio = 10
                # wall_height = self.screen.get_height()/((distance_hit)/ratio)
                # wall_rect = pygame.rect.Rect(i,self.screen.get_height()/2 - wall_height/2,1,wall_height)
                # pygame.draw.rect(self.screen,hit[1], wall_rect)

            self.player.draw(minimap, minimap_zoom)
            minimap_rect = pygame.rect.Rect((0, self.windows.get_height() - self.map.map_height * minimap_zoom), (self.map.map_width, self.map.map_height * minimap_zoom))
            self.windows.blit(minimap, minimap_rect)

            # flip() the display to put your work on screen
            pygame.display.flip()


            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()

jeu = game()