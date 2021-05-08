from Classes.Tiles import Tile


class Sack(Tile):
    def __init__(self, tile_groups, tile_image, pos_x, pos_y, size_x, size_y, game):
        super().__init__(tile_groups, tile_image, pos_x, pos_y, size_x, size_y)
        self.process_falling = False

    def fall(self, game, delta, kill_player):
        if self.pos_y == game.board.height - 1 or \
                game.level_map[self.pos_y + 1][self.pos_x] in ['T', 'F', 'S', 'G']:
            if self.process_falling:
                game.level_map[self.pos_y][self.pos_x] = 'G'
                self.kill()
                game.tiles[self.pos_y][self.pos_x] = Gold((game.gold_group, game.all_sprites),
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
            new_pos_y = round(self.rect.top / self.size_y)
            if self.pos_y != new_pos_y:
                if game.tiles[self.pos_y][self.pos_x] is self:
                    game.level_map[self.pos_y][self.pos_x] = '.'
                    game.tiles[self.pos_y][self.pos_x] = None
                if game.level_map[new_pos_y][self.pos_x] == 'M':
                    if game.tiles[self.pos_y][self.pos_x] is not None:
                        game.tiles[new_pos_y][self.pos_x].kill()
                    game.level_map[new_pos_y][self.pos_x] = 'S' if self is Sack else 'G'
                    game.tiles[new_pos_y][self.pos_x] = self
                elif game.level_map[new_pos_y][self.pos_x] == 'G':
                    if game.tiles[self.pos_y][self.pos_x] is not None:
                        game.tiles[self.pos_y][self.pos_x].kill()
                    game.level_map[new_pos_y][self.pos_x] = 'S' if self is Sack else 'G'
                    game.tiles[new_pos_y][self.pos_x] = self
                elif game.level_map[new_pos_y][self.pos_x] == 'P':
                    if kill_player:
                        game.status = 'Вас убил мешок с золотом!'
                        game.is_over = True
                    else:
                        self.kill()
                        game.score += 100
                self.pos_y = new_pos_y


class Gold(Sack):
    def __init__(self, tile_groups, tile_image, pos_x, pos_y, size_x, size_y, game):
        super().__init__(tile_groups, tile_image, pos_x, pos_y, size_x, size_y, game)
