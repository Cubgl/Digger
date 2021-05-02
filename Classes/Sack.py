from Classes.Tiles import Tile


class Sack(Tile):
    def __init__(self, tile_groups, tile_image, pos_x, pos_y, size_x, size_y, game):
        super().__init__(tile_groups, tile_image, pos_x, pos_y, size_x, size_y)
        self.process_falling = False

    def fall(self, game, delta):
        if self.pos_y == game.board.height - 1 or \
                game.level_map[self.pos_y + 1][self.pos_x] in ['T', 'F']:
            if self.process_falling:
                game.level_map[self.pos_y][self.pos_x] = 'G'
                self.kill()
                game.tiles[self.pos_y][self.pos_x] = Gold((game.sack_group, game.all_sprites),
                                                          game.tile_images['gold'], self.pos_x,
                                                          self.pos_y, self.size_x, self.size_y, game)
                self.process_falling = False
            return
        if self.pos_y + 1 < game.board.height and \
                game.level_map[self.pos_y + 1][self.pos_x] not in ['T', 'P', 'F'] and \
                not self.process_falling or self.process_falling and \
                game.level_map[self.pos_y + 1][self.pos_x] in ['.', 'M', 'P', 'G']:
            self.process_falling = True
            self.rect.top += delta
            game.level_map[self.pos_y][self.pos_x] = '.'
            self.pos_y = round(self.rect.top / self.size_y)
            if game.level_map[self.pos_y][self.pos_x] == 'M':
                game.tiles[self.pos_y][self.pos_x].kill()
                game.level_map[self.pos_y][self.pos_x] = '.'
            if game.level_map[self.pos_y][self.pos_x] == 'G':
                game.tiles[self.pos_y][self.pos_x].kill()
                game.level_map[self.pos_y][self.pos_x] = '.'
            if game.level_map[self.pos_y][self.pos_x] == 'P':
                game.is_over = True

class Gold(Sack):
    def __init__(self, tile_groups, tile_image, pos_x, pos_y, size_x, size_y, game):
        super().__init__(tile_groups, tile_image, pos_x, pos_y, size_x, size_y, game)

