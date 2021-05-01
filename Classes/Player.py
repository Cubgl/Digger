from Classes.Tiles import Tile


class Player(Tile):
    def __init__(self, player_groups, player_image, pos_x, pos_y, size_x, size_y):
        super().__init__(player_groups, player_image, pos_x, pos_y, size_x, size_y)

    def may_be_down(self, game):
        return self.rect.top + self.size_y < game.height_canvas

    def may_be_up(self, game):
        return self.rect.top - self.size_y >= 0

    def may_be_right(self, game):
        return self.rect.left + self.size_x < game.width_canvas

    def may_be_left(self, game):
        return self.rect.left - self.size_x >= 0

    def put_nothing(self, game):
        game.level_map[self.pos_y][self.pos_x] = '.'

    def go_down(self, game):
        self.put_nothing(game)
        self.rect.top += self.size_y
        self.pos_y += 1
        self.eat(game)

    def go_up(self, game):
        self.put_nothing(game)
        self.rect.top -= self.size_y
        self.pos_y -= 1
        self.eat(game)

    def go_right(self, game):
        self.put_nothing(game)
        self.rect.left += self.size_x
        self.pos_x += 1
        self.eat(game)

    def go_left(self, game):
        self.put_nothing(game)
        self.rect.left -= self.size_x
        self.pos_x -= 1
        self.eat(game)

    def eat(self, game):
        try:
            if game.level_map[self.pos_y][self.pos_x] == 'T':
                game.level_map[self.pos_y][self.pos_x] = 'P'
                game.tiles[self.pos_y][self.pos_x].kill()
                game.score += 1
            elif game.level_map[self.pos_y][self.pos_x] == 'G':
                game.level_map[self.pos_y][self.pos_x] = 'P'
                game.tiles[self.pos_y][self.pos_x].kill()
                game.score += 100
            elif game.level_map[self.pos_y][self.pos_x] == '.':
                game.level_map[self.pos_y][self.pos_x] = 'P'

        except IndexError as e:
            print(f'Position Player row={self.pos_y} col={self.pos_x}', e)
