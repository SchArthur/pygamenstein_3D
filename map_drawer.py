import pygame
from textureLoader import wallTexture

width = 1280
height = 720

wall_textures = wallTexture()

class drawer():
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((width,height))
        self.clock = pygame.time.Clock()


        canvas_size = (20,20)
        cell_size_width = self.screen.get_width() // canvas_size[0]
        cell_size_height = self.screen.get_height() // canvas_size[1]
        if cell_size_height < cell_size_width:
            self.cell_size = cell_size_height
        else :
            self.cell_size = cell_size_width

        self.canvas = pygame.surface.Surface((canvas_size[0] * self.cell_size, canvas_size[1] * self.cell_size))

        self.cell_list = []

        for x in range(canvas_size[0]):
            self.cell_list.append([])
            for y in range(canvas_size[1]):
                self.cell_list[x].append(cell((x,y), self.canvas, self.cell_size))


        self.run()

    def run(self):
        self.running = True
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed() :
                        pos = pygame.mouse.get_pos()
                        if self.canvas.get_rect().collidepoint(pos):
                            mouse_click_coords = (int(pos[0]//self.cell_size),int(pos[1]//self.cell_size))
                            if pygame.mouse.get_pressed()[0]:
                                self.cell_list[mouse_click_coords[0]][mouse_click_coords[1]].changeStatus(1)
                            elif pygame.mouse.get_pressed()[2]:
                                self.cell_list[mouse_click_coords[0]][mouse_click_coords[1]].changeStatus(-1)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        print('test')
                        self.saveMap()

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill('#C0C0C0')
            self.screen.blit(self.canvas, (0,0), self.canvas.get_rect())

            # flip() the display to put your work on screen
            pygame.display.flip()


            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()

    def saveMap(self):
        file = open('output.ini', 'w')
        content = ''
        for y in range(len(self.cell_list)):
            line = ''
            for x in range(len(self.cell_list[y])):
                value = str(self.cell_list[y][x].status +1)
                value += ',' 
                line += value
            line = line[:-1]
            content += line + '\n'
        content = content[:-1]
        file.write(content)
        file.close()
                

class cell():
    def __init__(self, pos, surface, cell_size, status = -1) -> None:
        self.position = pygame.Vector2(pos[0], pos[1])
        self.surface = surface
        self.cell_size = cell_size
        self.status = status
        self.draw()

    def draw(self):
        rect = pygame.rect.Rect(self.position.x * self.cell_size, self.position.y * self.cell_size, self.cell_size, self.cell_size)
        if self.status >= 0:
            texture = wall_textures.getWall(self.status)
            texture = pygame.transform.scale(texture, rect.size)
            self.surface.blit(texture, rect)
        else :
            pygame.draw.rect(self.surface, 'white', rect)

    def changeStatus(self, delta):
        self.status += delta
        if self.status < -1:
            self.status = -1
        elif self.status > len(wall_textures.hor_textures):
            self.status = len(wall_textures.hor_textures)
        self.draw()

draw= drawer()