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


class Sack(Tile):
    def __init__(self, tile_groups, tile_image, pos_x, pos_y, size_x, size_y, game):
        super().__init__(tile_groups, tile_image, pos_x, pos_y, size_x, size_y)
        self.process_falling = False

    def fall(self, game, delta):
        print(game.level_map[self.pos_y])
        if self.pos_y < game.board.height - 1:
            print(game.level_map[self.pos_y + 1])
        if self.pos_y == game.board.height - 1 or game.level_map[self.pos_y + 1][self.pos_x] == 'T':
            if self.process_falling:
                game.level_map[self.pos_y][self.pos_x] = 'G'
                self.kill()
                game.tiles[self.pos_y][self.pos_x] = Tile((game.tiles_group, game.all_sprites),
                                                          game.tile_images['gold'], self.pos_x,
                                                          self.pos_y, self.size_x, self.size_y)
                self.process_falling - False
            return
        if self.pos_y + 1 < game.board.height and game.level_map[self.pos_y + 1][self.pos_x] not in [
            'T', 'P']:
            self.process_falling = True
            self.rect.top += delta
            self.pos_y = round(self.rect.top / self.size_y)
            if game.level_map[self.pos_y][self.pos_x] == 'M':
                game.tiles[self.pos_y][self.pos_x].kill()
                game.level_map[self.pos_y][self.pos_x] == '.'
