from random import seed, randrange, choice, randint

LEVEL_PARAMS = {'level_1': {'size_x': 9, 'size_y': 7, 'monsters': 0, 'sacks': 0, 'gold': 10},
                'level_2': {'size_x': 10, 'size_y': 7, 'monsters': 0, 'sacks': 5, 'gold': 5},
                'level_3': {'size_x': 15, 'size_y': 15, 'monsters': 3, 'sacks': 10, 'gold': 10},
                'level_4': {'size_x': 20, 'size_y': 15, 'monsters': 3, 'sacks': 20, 'gold': 10},
                'level_5': {'size_x': 23, 'size_y': 20, 'monsters': 5, 'sacks': 15, 'gold': 15},
                'level_6': {'size_x': 29, 'size_y': 20, 'monsters': 5, 'sacks': 20, 'gold': 20},
                'level_7': {'size_x': 37, 'size_y': 25, 'monsters': 10, 'sacks': 20, 'gold': 20},
                'level_8': {'size_x': 43, 'size_y': 25, 'monsters': 10, 'sacks': 25, 'gold': 30},
                'level_9': {'size_x': 47, 'size_y': 25, 'monsters': 15, 'sacks': 30, 'gold': 30},
                'level_10': {'size_x': 60, 'size_y': 25, 'monsters': 15, 'sacks': 50, 'gold': 50}}


class GeneratorMap():
    def __init__(self, level):
        self.level = level
        seed()

    def generate_map(self, level):
        size = self.get_size_board(level)
        size_x = size[0]
        size_y = size[1]
        monsters = LEVEL_PARAMS[f'level_{level}']['monsters']
        sacks = LEVEL_PARAMS[f'level_{level}']['sacks']
        gold = LEVEL_PARAMS[f'level_{level}']['gold']
        total = size_x * size_y
        free = total - monsters - sacks - gold
        map = []
        for i in range(size_y):
            map.append(list(' ' * size_x))
        if self.level > 5:
            self.random_way(size_x, size_y, map, round(free * 5 / 6))
        else:
            self.random_way(size_x, size_y, map, free // 2)
        self.fill_other_as_terrain(map)
        self.put_monsters(size_x, size_y, map, monsters)
        self.put_gold(size_x, size_y, map, gold)
        self.put_sacks(size_x, size_y, map, sacks)
        self.put_single(size_x, size_y, map, 'P')
        self.put_single(size_x, size_y, map, 'F')
        self.print_map(map)
        return size, map

    def get_size_board(self, level):
        return LEVEL_PARAMS[f'level_{level}']['size_x'], LEVEL_PARAMS[f'level_{level}']['size_y']

    def into_map(self, x, y, size_x, size_y):
        return (0 <= x < size_x) and (0 <= y < size_y)

    def random_way(self, size_x, size_y, map, count):
        first_x = randrange(0, size_x)
        first_y = randrange(0, size_y)
        map[first_y][first_x] = '.'
        count -= 1
        while count:
            while True:
                dx, dy = choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
                if self.into_map(first_x + dx, first_y + dy, size_x, size_y):
                    x, y = first_x + dx, first_y + dy
                    break
            map[y][x] = '.'
            first_x, first_y = x, y
            count -= 1

    def print_map(self, map):
        for line in map:
            print(''.join(line))

    def fill_other_as_terrain(self, map):
        for y in range(len(map)):
            for x in range(len(map[y])):
                if map[y][x] == ' ':
                    map[y][x] = 'T'

    def take_random_tile(self, size_x, size_y, map, ch):
        x, y = randrange(0, size_x), randrange(0, size_y)
        while map[y][x] != ch:
            x, y = randrange(0, size_x), randrange(0, size_y)
        return x, y

    def take_random_near(self, size_x, size_y, map, x, y, ch):
        near_x, near_y = None, None
        attempts = 0
        while attempts <= 10:
            dx, dy = choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            if self.into_map(x + dx, y + dy, size_x, size_y) and map[y + dy][x + dx] == ch:
                near_x, near_y = x + dx, y + dy
                break
            attempts += 1
        success = attempts <= 10
        return success, near_x, near_y

    def put_one_monster(self, size_x, size_y, map):
        x, y = self.take_random_tile(size_x, size_y, map, '.')
        start_x, start_y = x, y
        map[y][x] = 'M'
        count_space_near = randint(1, 7)
        for i in range(count_space_near):
            founded, near_x, near_y = self.take_random_near(size_x, size_y, map, x, y, '.')
            if founded:
                x, y = near_x, near_y
                map[y][x] = '.'
            else:
                x, y = start_x, start_y

    def put_monsters(self, size_x, size_y, map, count_monsters):
        for i in range(count_monsters):
            self.put_one_monster(size_x, size_y, map)

    def count_around(self, x, y, size_x, size_y):
        count = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if self.into_map(x + dx, y + dy, size_x, size_y) and not (dx == 0 and dy == 0):
                    count += 1
        return count

    def tiles_around(self, x, y, size_x, size_y, map, ch):
        count = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if self.into_map(x + dx, y + dy, size_x, size_y) and \
                        not (dx == 0 and dy == 0) and map[y + dy][x + dx] == ch:
                    count += 1
        return count

    def put_single(self, size_x, size_y, map, ch):
        if map[0][0] == 'T' and \
                self.count_around(0, 0, size_x, size_y) == \
                self.tiles_around(0, 0, size_x, size_y, map, 'T'):
            map[0][0] = ch
            return
        if map[0][size_x - 1] == 'T' and \
                self.count_around(size_x - 1, 0, size_x, size_y) == \
                self.tiles_around(size_x - 1, 0, size_x, size_y, map, 'T'):
            map[0][size_x - 1] = ch
            return
        if map[size_y - 1][0] == 'T' and \
                self.count_around(0, size_y - 1, size_x, size_y) == \
                self.tiles_around(0, size_y - 1, size_x, size_y, map, 'T'):
            map[size_y - 1][0] = ch
            return
        if map[size_y - 1][size_x - 1] == 'T' and \
                self.count_around(size_x - 1, size_y - 1, size_x, size_y) == \
                self.tiles_around(size_x - 1, size_y - 1, size_x, size_y, map, 'T'):
            map[size_y - 1][size_x - 1] = ch
            return
        x, y = self.take_random_tile(size_x, size_y, map, 'T')
        for attempt in range(77):
            if map[y][x] == 'T' and \
                    self.count_around(x, y, size_x, size_y) == \
                    self.tiles_around(x, y, size_x, size_y, map, 'T'):
                break
            x, y = self.take_random_tile(size_x, size_y, map, 'T')
        map[y][x] = ch

    def put_gold(self, size_x, size_y, map, count_gold):
        for i in range(count_gold):
            self.put_one_gold(size_x, size_y, map)

    def put_one_gold(self, size_x, size_y, map):
        for attempt in range(7):
            x, y = self.take_random_tile(size_x, size_y, map, 'T')
            if y == size_y - 1:
                map[y][x] = 'G'
                return
            if map[y + 1][x] == 'T':
                map[y][x] = 'G'
                return

    def put_sacks(self, size_x, size_y, map, count_sacks):
        for i in range(count_sacks):
            self.put_one_sack(size_x, size_y, map)

    def put_one_sack(self, size_x, size_y, map):
        for attempt in range(7):
            x, y = self.take_random_tile(size_x, size_y - 1, map, 'T')
            if y > 0 and (map[y - 1][x] == 'S' or map[y - 1][x] == 'G'):
                continue
            if map[y + 1][x] == 'T':
                map[y][x] = 'S'
                return
