import pygame
import math

wall_color = 'black'

class newMap():
    def __init__(self, filePath) -> None:
        #recupere le contenu du fichier de la map
        file = open(filePath, 'r')
        self.file_content = file.readlines()
        file.close()

        self.setCells()

    def setCells(self):
        self.cells = []
        for line in self.file_content :
            self.cells.append(line.strip().split(','))

    def getMiniMap(self) -> pygame.surface.Surface :
        self.map_height = len(self.cells)
        self.map_width = len(self.cells[0])
        surface = pygame.surface.Surface((self.map_width, self.map_height))
        surface.fill('white')
        for y in range(len(self.cells)):
            for x in range(len(self.cells[y])):
                if self.cells[y][x] == '1':
                    cell_rect = pygame.rect.Rect((x,y),(1,1))
                    pygame.draw.rect(surface, wall_color, cell_rect)

        return surface
    
    def hasHitWall(self, ray_pos : pygame.Vector2) -> bool:
        isWall = False
        max_x = len(self.cells[0])
        max_y = len(self.cells)

        if ray_pos.x < 1 or ray_pos.x > max_x or ray_pos.y < 1 or ray_pos.y > max_y:
            isWall = True
        else:
            if not ray_pos.x.is_integer():
                x = int(math.floor(ray_pos.x))
                y_1 = int(ray_pos.y)
                y_2 = y_1 - 1
                if self.cells[y_1][x] == '1' or self.cells[y_2][x] == '1':
                    isWall = True
            elif not ray_pos.y.is_integer():
                y = int(math.floor(ray_pos.y))
                x_1 = int(ray_pos.x)
                x_2 = x_1 - 1
                if self.cells[y][x_1] == '1' or self.cells[y][x_2] == '1':
                    isWall = True

        return isWall


# cells = newMap('map_1.ini')
# coords_test = pygame.Vector2(15.2,2)
# print(cells.hasHitWall(coords_test))