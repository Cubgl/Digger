import os
import sys
from pprint import pprint

import pygame

from Classes.Board import BoardGame
from Classes.Generator import GeneratorMap
from Classes.Monster import Monster
from Classes.Player import Player
from Classes.Sack import Sack, Gold
from Classes.Tiles import Tile, Finish

TILE_WIDTH = 32
TILE_HEIGHT = 32


class GameDigger:
    def __init__(self):
        self.level = 0
        self.count_levels = 10
        self.dificult = 2
        self.score = 0
        self.size_board = None
        self.level_map = None
        self.board = BoardGame(1,1)
        self.is_over = False
        self.tile_images = {'gold': self.load_image('Gold.png'),
                            'monster': self.load_image('Monster.png'),
                            'sack': self.load_image('Sack.png'),
                            'terrain': self.load_image('Terrain.png'),
                            'finish': self.load_image('door.png')}
        self.player_image = self.load_dict_images('Digger', '.png')
        self.all_sprites = pygame.sprite.Group()
        self.tiles_group = pygame.sprite.Group()
        self.sack_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.monster_group = pygame.sprite.Group()
        self.finish_group = pygame.sprite.Group()
        self.new_game = True
        self.image_background = pygame.Surface([32, 32])
        self.image_background.fill(pygame.Color("black"))
        self.goto_next_level(None)

    def goto_next_level(self, scr):
        self.level += 1
        if self.level > self.count_levels:
            self.is_over = True
            print(f'Игра зкончилась! Счет {self.score}.')
            return
        if not self.new_game:
            for y in range(self.size_board[1]):
                for x in range(self.size_board[0]):
                    if self.tiles[y][x] is not None:
                        self.tiles[y][x].kill()
            for sprt in self.all_sprites.sprites():
                sprt.kill()

            self.all_sprites.clear(scr, self.image_background)
        else:
            self.new_game = False
        self.take_level()
        self.board.change_size(self.size_board[0], self.size_board[1])
        self.width_canvas, self.height_canvas = self.resize_canvas(self.board)
        self.tiles = []
        for y in range(self.size_board[1]):
            self.tiles.append([None] * self.size_board[0])
        self.player = self.generate_level(self.level_map)

    def take_level(self):
        if self.dificult == 1:
            self.size_board, self.level_map = self.load_level(f'level{self.level}.map')
        elif self.dificult == 2:
            generator = GeneratorMap(self.level)
            self.size_board, self.level_map = generator.generate_map(self.level)

    def load_dict_images(self, the_begin_filename, the_end_filename):
        dict_for_image = dict()
        dict_for_image['left'] = self.load_image(the_begin_filename + '_left' + the_end_filename)
        dict_for_image['right'] = self.load_image(the_begin_filename + '_right' + the_end_filename)
        dict_for_image['up'] = self.load_image(the_begin_filename + '_up' + the_end_filename)
        dict_for_image['down'] = self.load_image(the_begin_filename + '_down' + the_end_filename)
        return dict_for_image

    def resize_canvas(self, board):
        new_width = board.width * board.cell_size
        new_height = board.height * board.cell_size
        return new_width, new_height

    def load_level(self, filename):
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [list(line.strip()) for line in mapFile]
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

    def generate_level(self, level_map):
        new_player = None
        for y in range(len(level_map)):
            for x in range(len(level_map[y])):
                if level_map[y][x] == 'P':
                    new_player = Player((self.player_group, self.all_sprites),
                                        self.player_image['right'], x, y, TILE_WIDTH, TILE_HEIGHT)
                    self.tiles[y][x] = new_player
                elif level_map[y][x] == 'T':
                    self.tiles[y][x] = Tile((self.tiles_group, self.all_sprites),
                                            self.tile_images['terrain'], x, y, TILE_WIDTH,
                                            TILE_HEIGHT)
                elif level_map[y][x] == 'S':
                    self.tiles[y][x] = Sack((self.sack_group, self.all_sprites),
                                            self.tile_images['sack'], x, y, TILE_WIDTH, TILE_HEIGHT,
                                            self)
                elif level_map[y][x] == 'G':
                    self.tiles[y][x] = Gold((self.sack_group, self.all_sprites),
                                            self.tile_images['gold'], x, y, TILE_WIDTH, TILE_HEIGHT,
                                            self)
                elif level_map[y][x] == 'M':
                    self.tiles[y][x] = Monster((self.monster_group, self.all_sprites),
                                               self.tile_images['monster'], x, y, TILE_WIDTH,
                                               TILE_HEIGHT, self)
                elif level_map[y][x] == 'F':
                    self.tiles[y][x] = Finish((self.finish_group, self.all_sprites),
                                               self.tile_images['finish'], x, y, TILE_WIDTH,
                                               TILE_HEIGHT)
        return new_player
