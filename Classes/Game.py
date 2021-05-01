import os
import sys

import pygame

from Classes.Board import BoardGame
from Classes.Player import Player
from Classes.Tiles import Tile, Sack

TILE_WIDTH = 32
TILE_HEIGHT = 32


class GameDigger:
    def __init__(self):
        self.level = 3
        self.count_levels = 3
        self.size_board, self.level_map = self.load_level(f'level{self.level}.map')
        self.board = BoardGame(self.size_board[0], self.size_board[1])
        self.width_canvas, self.height_canvas = self.resize_canvas(self.board)
        self.score = 0
        self.is_over = False
        self.tile_images = {'gold': self.load_image('Gold.png'),
                            'monster': self.load_image('Monster.png'),
                            'sack': self.load_image('Sack.png'),
                            'terrain': self.load_image('Terrain.png'),
                            'nothing': self.load_image('Nothing.png')}
        self.player_image = self.load_image('Digger.png')
        self.all_sprites = pygame.sprite.Group()
        self.tiles_group = pygame.sprite.Group()
        self.sack_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.tiles = []
        for i in range(self.size_board[1]):
            self.tiles.append([None] * self.size_board[0])
        self.player = self.generate_level(self.level_map)

    def resize_canvas(self, board):
        new_width = board.width * board.cell_size
        new_height = board.height * board.cell_size
        return new_width, new_height

    def load_level(self, filename):
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [list(line.strip()) for line in mapFile]
        # for i in range(len(level_map)):
        #     print(f'{i}: {level_map[i]}')
        width = max(map(len, level_map))
        height = len(level_map)
        return (width, height), level_map

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('images', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        return image

    def change_level(self):
        self.level += 1
        if self.level > self.count_levels:
            self.is_over = True
            print(f'Игра зкончилась! Счет {self.score}.')
            sys.exit(0)
        self.size_board, self.level_map = self.load_level(f'level{self.level}.map')
        self.board.change_size(self.size_board[0], self.size_board[1])
        self.resize_canvas(self.board)

    def generate_level(self, level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == 'P':
                    new_player = Player((self.player_group, self.all_sprites),
                                        self.player_image, x, y, TILE_WIDTH, TILE_HEIGHT)
                    self.tiles[y][x] = new_player
                elif level[y][x] == 'T':
                    self.tiles[y][x] = Tile((self.tiles_group, self.all_sprites),
                                            self.tile_images['terrain'], x, y, TILE_WIDTH,
                                            TILE_HEIGHT)
                elif level[y][x] == 'S':
                    self.tiles[y][x] = Sack((self.sack_group, self.all_sprites),
                                            self.tile_images['sack'], x, y, TILE_WIDTH, TILE_HEIGHT,
                                            self)
                elif level[y][x] == 'G':
                    self.tiles[y][x] = Tile((self.tiles_group, self.all_sprites),
                                            self.tile_images['gold'], x, y, TILE_WIDTH, TILE_HEIGHT)
                elif level[y][x] == 'M':
                    self.tiles[y][x] = Tile((self.tiles_group, self.all_sprites),
                                            self.tile_images['monster'], x, y, TILE_WIDTH,
                                            TILE_HEIGHT)
                # elif level[y][x] == '.':
                #     self.tiles[y][x] = Tile((self.tiles_group, self.all_sprites),
                #                             self.tile_images['nothing'], x, y, TILE_WIDTH,
                #                             TILE_HEIGHT)

        return new_player
