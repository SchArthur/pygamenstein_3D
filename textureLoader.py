import pygame
from PIL import Image

class wallTexture():
    def __init__(self) -> None:
        file = Image.open('walls.png')
        file = file.convert('RGB')
        self.texture = file.load()
        size = file.size
        file.close()

        offset = 8
        self.wall_size = 32
        textures_per_row = 8
        textures_per_col = 8
        self.textures_list = []
        for i in range(textures_per_col):
            y_offset = (offset * (i+1)) + (self.wall_size * i)
            for j in range(textures_per_row):
                x_offset = (offset * (j+1)) + (self.wall_size * j)
                new_texture = Image.new('RGB', (self.wall_size, self.wall_size))
                new_texture_data = new_texture.load()
                for y in range(self.wall_size):
                    for x in range(self.wall_size):
                        x_coords = x_offset + x
                        y_coords = y_offset + y
                        color = self.texture[x_coords,y_coords]
                        new_texture_data[x,y] = color
                wall = new_texture.copy()
                self.textures_list.append(wall)

        self.ver_textures = []
        self.hor_textures = []

        for i in range(len(self.textures_list)):
            if (i % 2) != 0:
                self.ver_textures.append(self.textures_list[i])
            else :
                self.hor_textures.append(self.textures_list[i])


    def getStripe(self, coords, texture_index : str, texture_type : str) -> pygame.surface:
        stripe = pygame.surface.Surface((1,self.wall_size))
        self.texture_x = int(coords * self.wall_size)
        if texture_type == 'hor':
            texture = self.hor_textures[texture_index].load()
        elif texture_type == 'ver':
            texture = self.ver_textures[texture_index].load()
            
        for y in range(stripe.get_height()):
            stripe.set_at((0, y), texture[self.texture_x, y])

        return stripe
