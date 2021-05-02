from random import choice

from Classes.Tiles import Tile


class Monster(Tile):
    def __init__(self, player_groups, player_image, pos_x, pos_y, size_x, size_y, game):
        super().__init__(player_groups, player_image, pos_x, pos_y, size_x, size_y)
        self.game = game

        self.action = self.select_attack(game.level)
        self.direction = choice(['vert', 'horiz'])
        self.select_direction()
        self.sub_direction = self.select_subdirection()


    def select_attack(self, level):
        return self.do_nothing
        # if level == 3:
        #     return self.do_nothing
        # if level == 4:
        #     return self.do_nothing
        # if level == 5:
        #     return self.do_nothing

    def do_nothing(self, delta):
        pass

    def into_map(self, x, y, size_x, size_y):
        return 0 <= x < size_x and 0 <= y < size_y

    def may_go_horiz(self, x, y, map):
        size_map_x, size_map_y = len(map[0]), len(map)
        left_x, left_y = x - 1, y
        if self.into_map(left_x, left_y, size_map_x, size_map_y) and map[left_y][left_x] == '.':
            return True
        right_x, right_y = x + 1, y
        if self.into_map(right_x, right_y, size_map_x, size_map_y) and map[right_y][right_x] == '.':
            return True
        return False

    def may_go_vert(self, x, y, map):
        size_map_x, size_map_y = len(map[0]), len(map)
        up_x, up_y = x, y - 1
        if self.into_map(up_x, up_y, size_map_x, size_map_y) and map[up_y][up_x] == '.':
            return True
        down_x, down_y = x, y + 1
        if self.into_map(down_x, down_y, size_map_x, size_map_y) and map[down_y][down_x] == '.':
            return True
        return False

    def select_direction(self):
        if not self.may_go_vert(self.pos_x, self.pos_y, self.game.level_map) and \
                not self.may_go_horiz(self.pos_x, self.pos_y, self.game.level_map):
            self.action = self.do_nothing
            self.direction = 'no_direction'
            return
        if self.direction == 'vert' and \
            not self.may_go_vert(self.pos_x, self.pos_y, self.game.level_map):
            self.direction = 'horiz'
        if self.direction == 'horiz' and \
                not self.may_go_horiz(self.pos_x, self.pos_y, self.game.level_map):
            self.direction = 'vert'

    def select_subdirection(self):
        if self.direction == 'vert':
            return choice(['up', 'down'])
        elif self.direction == 'horiz':
            return choice(['left', 'right'])

    def go_around(self):
        pass









