import sys
from pprint import pprint
from random import choice

from Classes.Tiles import Tile


class Monster(Tile):
    def __init__(self, player_groups, player_image, pos_x, pos_y, size_x, size_y, game):
        super().__init__(player_groups, player_image, pos_x, pos_y, size_x, size_y)
        self.game = game
        if self.game.level <= 5:
            self.delta = 1
        else:
            self.delta = 2
        self.direction = 'no_direction'
        self.select_direction()
        self.sub_direction = self.select_subdirection()
        self.to_x, self.to_y = self.pos_x, self.pos_y
        self.way = []
        self.action = self.select_attack(game.level)

    def select_attack(self, level):
        if level <= 3:
            return self.do_nothing
        if 3 < level <= 5:
            return self.go_around
        if level > 5:
            return self.go_three_steps

    def do_nothing(self):
        pass

    def into_map(self, x, y, size_x, size_y):
        return 0 <= x < size_x and 0 <= y < size_y

    def may_go_left(self, x, y, size_map_x, size_map_y, map):
        left_x, left_y = x - 1, y
        return self.into_map(left_x, left_y, size_map_x, size_map_y) and \
               map[left_y][left_x] in ['.', 'P']

    def may_go_right(self, x, y, size_map_x, size_map_y, map):
        right_x, right_y = x + 1, y
        return self.into_map(right_x, right_y, size_map_x, size_map_y) and \
               map[right_y][right_x] in ['.', 'P']

    def may_go_horiz(self, x, y, map):
        size_map_x, size_map_y = len(map[0]), len(map)
        return self.may_go_left(x, y, size_map_x, size_map_y, map) or \
            self.may_go_right(x, y, size_map_x, size_map_y, map)

    def may_go_up(self, x, y, size_map_x, size_map_y, map):
        up_x, up_y = x, y - 1
        return self.into_map(up_x, up_y, size_map_x, size_map_y) and map[up_y][up_x] in ['.', 'P']

    def may_go_down(self, x, y, size_map_x, size_map_y, map):
        down_x, down_y = x, y + 1
        return self.into_map(down_x, down_y, size_map_x, size_map_y) and \
               map[down_y][down_x] in ['.', 'P']

    def may_go_vert(self, x, y, map):
        size_map_x, size_map_y = len(map[0]), len(map)
        return self.may_go_up(x, y, size_map_x, size_map_y, map) or \
               self.may_go_down(x, y, size_map_x, size_map_y, map)

    def select_direction(self):
        self.direction = choice(['vert', 'horiz'])
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

    def search_point(self, x, y, size_map_x, size_map_y, map):
        if self.direction == 'horiz' and self.sub_direction == 'left':
            finish_x, finish_y = x, y
            while self.may_go_left(finish_x, finish_y, size_map_x, size_map_y, map):
                finish_x = finish_x - 1
            return finish_x, finish_y
        if self.direction == 'horiz' and self.sub_direction == 'right':
            finish_x, finish_y = x, y
            while self.may_go_right(finish_x, finish_y, size_map_x, size_map_y, map):
                finish_x = finish_x + 1
            return finish_x, finish_y
        if self.direction == 'vert' and self.sub_direction == 'up':
            finish_x, finish_y = x, y
            while self.may_go_up(finish_x, finish_y, size_map_x, size_map_y, map):
                finish_y = finish_y - 1
            return finish_x, finish_y
        if self.direction == 'vert' and self.sub_direction == 'down':
            finish_x, finish_y = x, y
            while self.may_go_down(finish_x, finish_y, size_map_x, size_map_y, map):
                finish_y = finish_y + 1
            return finish_x, finish_y
        return -1, -1

    def step(self):
        if self.direction == 'horiz' and self.sub_direction == 'left':
            self.rect.left -= self.delta
            new_pos_x = (self.rect.left + self.size_x) // self.size_x
            if new_pos_x != self.pos_x:
                if self.game.tiles[self.pos_y][self.pos_x] is self:
                    self.game.level_map[self.pos_y][self.pos_x] = '.'
                    self.game.tiles[self.pos_y][self.pos_x] = None
                if self.game.tiles[self.pos_y][new_pos_x] is None:
                    self.game.level_map[self.pos_y][new_pos_x] = 'M'
                    self.game.tiles[self.pos_y][new_pos_x] = self
                self.pos_x = new_pos_x

        if self.direction == 'horiz' and self.sub_direction == 'right':
            self.rect.left += self.delta
            new_pos_x = self.rect.left // self.size_x
            if new_pos_x != self.pos_x:
                if self.game.tiles[self.pos_y][self.pos_x] is self:
                    self.game.level_map[self.pos_y][self.pos_x] = '.'
                    self.game.tiles[self.pos_y][self.pos_x] = None
                if self.game.tiles[self.pos_y][new_pos_x] is None:
                    self.game.level_map[self.pos_y][new_pos_x] = 'M'
                    self.game.tiles[self.pos_y][new_pos_x] = self
                self.pos_x = new_pos_x

        if self.direction == 'vert' and self.sub_direction == 'up':
            self.rect.top -= self.delta
            new_pos_y = (self.rect.top + self.size_y) // self.size_y
            if new_pos_y != self.pos_y:
                if self.game.tiles[self.pos_y][self.pos_x] is self:
                    self.game.level_map[self.pos_y][self.pos_x] = '.'
                    self.game.tiles[self.pos_y][self.pos_x] = None
                if self.game.tiles[new_pos_y][self.pos_x] is None:
                    self.game.level_map[new_pos_y][self.pos_x] = 'M'
                    self.game.tiles[new_pos_y][self.pos_x] = self
                self.pos_y = new_pos_y

        if self.direction == 'vert' and self.sub_direction == 'down':
            self.rect.top += self.delta
            new_pos_y = self.rect.top // self.size_y
            if new_pos_y != self.pos_y:
                if self.game.tiles[self.pos_y][self.pos_x] is self:
                    self.game.level_map[self.pos_y][self.pos_x] = '.'
                    self.game.tiles[self.pos_y][self.pos_x] = None
                if self.game.tiles[new_pos_y][self.pos_x] is None:
                    self.game.level_map[new_pos_y][self.pos_x] = 'M'
                    self.game.tiles[new_pos_y][self.pos_x] = self
                self.pos_y = new_pos_y

    def success_step(self, to_x, to_y):
        self.step()
        if self.pos_x == to_x and self.pos_y == to_y:
            return False
        return True

    def go_around(self):
        if self.direction == 'no_direction':
            return
        map = self.game.level_map
        size_map_x, size_map_y = len(map[0]), len(map)
        while self.to_x == self.pos_x and self.to_y == self.pos_y:
            self.to_x, self.to_y = self.search_point(self.pos_x, self.pos_y, size_map_x, size_map_y, map)
            if self.to_x == self.pos_x and self.to_y == self.pos_y:
                self.sub_direction = self.select_subdirection()
        if not self.success_step(self.to_x, self.to_y):
            self.select_direction()
            self.sub_direction = self.select_subdirection()

    def dist_manh(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def dist_eq(self, x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def bfs(self, x, y, goal_x, goal_y, map):
        size_map_x, size_map_y = len(map[0]), len(map)
        min_d = self.dist_eq(x, y, goal_x, goal_y)
        queue = [(x, y, 0, min_d)]
        used = set()
        used.add((x, y))
        i = 0
        while i < len(queue):
            cur_x, cur_y, cur_steps, _ = queue[i]
            if cur_steps == 5:
                break
            if self.may_go_left(cur_x, cur_y, size_map_x, size_map_y, map) and \
                    (cur_x - 1, cur_y) not in used:
                used.add((cur_x - 1, cur_y))
                d = self.dist_eq(cur_x - 1, cur_y, goal_x, goal_y)
                queue.append((cur_x - 1, cur_y, cur_steps + 1, d))
                if d < min_d:
                    min_d = d
                if cur_x - 1 == goal_x and cur_y == goal_y:
                    break
            if self.may_go_right(cur_x, cur_y, size_map_x, size_map_y, map) and \
                    (cur_x + 1, cur_y) not in used:
                used.add((cur_x + 1, cur_y))
                d = self.dist_eq(cur_x + 1, cur_y, goal_x, goal_y)
                queue.append((cur_x + 1, cur_y, cur_steps + 1, d))
                if d < min_d:
                    min_d = d
                if cur_x + 1 == goal_x and cur_y == goal_y:
                    break
            if self.may_go_up(cur_x, cur_y, size_map_x, size_map_y, map) and \
                    (cur_x, cur_y - 1) not in used:
                used.add((cur_x, cur_y - 1))
                d = self.dist_eq(cur_x, cur_y - 1, goal_x, goal_y)
                queue.append((cur_x, cur_y - 1, cur_steps + 1, d))
                if d < min_d:
                    min_d = d
                if cur_x == goal_x and cur_y - 1 == goal_y:
                    break
            if self.may_go_down(cur_x, cur_y, size_map_x, size_map_y, map) and \
                    (cur_x, cur_y + 1) not in used:
                used.add((cur_x, cur_y + 1))
                d = self.dist_eq(cur_x, cur_y + 1, goal_x, goal_y)
                queue.append((cur_x, cur_y + 1, cur_steps + 1, d))
                if d < min_d:
                    min_d = d
                if cur_x == goal_x and cur_y + 1 == goal_y:
                    break
            i += 1
        # print(len(queue))
        return queue, min_d

    def get_way(self, queue, min_d):
        levels = {}
        i = 0
        cur_steps = None
        rez = []
        while i < len(queue):
            x, y, steps, d = queue[i]
            if steps in levels:
                levels[steps].append((x, y, d))
            else:
                levels[steps] = [(x, y, d)]
            if d == min_d:
                rez = [(x, y)]
                cur_steps = steps
                break
            i += 1
        while cur_steps > 0:
            cur_steps -= 1
            mini = 100000
            min_value = None
            for elem in levels[cur_steps]:
                if self.dist_manh(rez[-1][0], rez[-1][1], elem[0], elem[1]) == 1 and elem[2] < mini:
                    mini = elem[2]
                    min_value = (elem[0], elem[1])
            rez.append(min_value)
        return list(reversed(rez))

    def go_three_steps(self):
        if self.game.level_map[self.pos_y][self.pos_x] == 'T':
            print(f'WALL !!! pos x {self.pos_x}, y {self.pos_y} ')
            print(self.way)
            print()
            for elem in self.game.level_map:
                print(''.join(elem))
            sys.exit()


        # print(f'pos x {self.pos_x}, y {self.pos_y}')
        # print(f'to x {self.to_x} y {self.to_y}')

        if self.way is None or len(self.way) == 0:
            goal_x, goal_y = self.game.player.pos_x, self.game.player.pos_y
            # print(f'Goal x = {goal_x}, y = {goal_y}')

            queue, min_dist = self.bfs(self.pos_x, self.pos_y, goal_x, goal_y, self.game.level_map)
            # print(f'queue = {queue}, min_dist = {min_dist}')
            self.way = self.get_way(queue, min_dist)
            # print(self.way)
        else:
            if self.pos_x == self.to_x and self.pos_y == self.to_y:
                if self.pos_x == self.way[0][0] and self.pos_y == self.way[0][1]:
                    self.pos_x, self.pos_y = self.way[0]
                    self.way = self.way[1:]
                # print(f'pos x {self.pos_x}, y {self.pos_y}')
                if len(self.way) != 0:
                    self.to_x, self.to_y = self.way[0]
                    # print(f'    to x {self.to_x} y {self.to_y}')
                    self.way = self.way[1:]
                    if self.game.level_map[self.to_y][self.to_x] in ['P', '.']:
                        if self.to_x == self.pos_x:
                            self.direction = 'vert'
                            if self.to_y > self.pos_y:
                                self.sub_direction = 'down'
                            else:
                                self.sub_direction = 'up'
                        elif self.to_y == self.pos_y:
                            self.direction = 'horiz'
                            if self.to_x > self.pos_x:
                                self.sub_direction = 'right'
                            else:
                                self.sub_direction = 'left'
                    else:
                        self.way = []
                        self.to_x, self.to_y = self.pos_x, self.pos_y
                else:
                    self.way = []
                    self.to_x, self.to_y = self.pos_x, self.pos_y
            else:
                self.step()














