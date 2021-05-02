import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_groups, tile_image, pos_x, pos_y, size_x, size_y):
        super().__init__(*tile_groups)
        self.image = tile_image
        self.pos_y = pos_y
        self.pos_x = pos_x
        self.size_x = size_x
        self.size_y = size_y
        self.rect = self.image.get_rect().move(self.size_x * pos_x, self.size_y * pos_y)

class Finish(Tile):
    def __init__(self, tile_groups, tile_image, pos_x, pos_y, size_x, size_y):
        super().__init__(tile_groups, tile_image, pos_x, pos_y, size_x, size_y)