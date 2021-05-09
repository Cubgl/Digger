import sys

import pygame

from Classes.Game import GameDigger

START_WIDTH, START_HEIGHT = 750, 550


pygame.init()
game = GameDigger()
size = game.width_canvas, game.height_canvas


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ДИГГЕР", "",
                  "Правила игры",
                  "Диггер - подземный житель, он умеет рыть",
                  "ходы в земле и собирать золото, которое",
                  "бывает в мешках и без них.",
                  "Цель игры: собрать как можно больше золота.",
                  "На пути диггеру могут встретиться монстры,",
                  "от них надо убегать. При столкновении",
                  "с монстром диггер умирает. Чтобы собрать",
                  "золото из мешка, его нужно сначала уронить,",
                  "иными словами сделать так, чтобы мешок упал ",
                  "вниз. Монстра можно задавить падающим мешком,",
                  "за это будут дополнительные очки. Когда все",
                  'золото на уровне собрано, идите к "двери",',
                  "через нее приоисходит переход на новый уровень.",
                  "Управляется диггер стрелочками. Удачи в игре!",
                  ""
                  "Для начала игры нажмите любую клавишу..."]
    screen = pygame.display.set_mode((START_WIDTH, START_HEIGHT))
    fon = pygame.transform.scale(game.load_image('digger_start.png'), (START_WIDTH, START_HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 5
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 210
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(50)


start_screen()
screen = [None] * (game.count_levels + 1)
keys = [None] * (game.count_levels + 1)
screen[game.level] = pygame.display.set_mode(size)
keys[game.level] = [False] * 512


def kill_monsters(dict_collision):
    for key, val in dict_collision.items():
        if key.process_falling:
            for monster in val:
                monster.kill()
                game.score += 500


def main():
    running = True
    v = 60
    fps = 60
    pygame.display.set_caption(f'Score = {game.score}')
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys[game.level] = pygame.key.get_pressed()
            if keys[game.level][pygame.K_DOWN]:
                if game.player.may_be_down(game):
                    game.player.image = game.player_image['down']
                    game.player.go_down(game)
            elif keys[game.level][pygame.K_UP]:
                if game.player.may_be_up(game):
                    game.player.image = game.player_image['up']
                    game.player.go_up(game)
            elif keys[game.level][pygame.K_RIGHT]:
                if game.player.may_be_right(game):
                    game.player.image = game.player_image['right']
                    game.player.go_right(game)
            elif keys[game.level][pygame.K_LEFT]:
                if game.player.may_be_left(game):
                    game.player.image = game.player_image['left']
                    game.player.go_left(game)
        screen[game.level].fill((0, 0, 0))
        game.all_sprites.draw(screen[game.level])
        pygame.display.set_caption(f'Score = {game.score}, Level = {game.level}')
        for sack in game.sack_group.sprites():
            sack.fall(game, v / fps, True)
        for gold in game.gold_group.sprites():
            gold.fall(game, v / fps, False)
        for monster in game.monster_group.sprites():
            monster.action()
        kill_monsters(pygame.sprite.groupcollide(game.gold_group, game.monster_group, False, False,
                                                 collided=pygame.sprite.collide_rect_ratio(.75)))
        kill_monsters(pygame.sprite.groupcollide(game.sack_group, game.monster_group, False, False,
                                                 collided=pygame.sprite.collide_rect_ratio(.75)))
        pygame.sprite.groupcollide(game.sack_group, game.gold_group, True, False,
                                   collided=pygame.sprite.collide_rect_ratio(.75))
        pygame.sprite.groupcollide(game.tiles_group, game.monster_group, False, False,
                                   collided=pygame.sprite.collide_rect_ratio(.75))
        if pygame.sprite.spritecollideany(game.player, game.monster_group,
                                          collided=pygame.sprite.collide_rect_ratio(
                                              .75)) is not None:
            game.status = "Вас съел Монстр!"
            game.is_over = True
        if pygame.sprite.spritecollideany(
                game.player, game.finish_group, collided=pygame.sprite.collide_rect_ratio(.75)) \
                is not None and len(game.sack_group.sprites()) == 0 and \
                len(game.gold_group.sprites()) == 0:
            game.goto_next_level(screen[game.level])
            if not game.is_over:
                size = game.width_canvas, game.height_canvas
                screen[game.level] = pygame.display.set_mode(size)
                keys[game.level] = [False] * 512
        if game.is_over:
            running = False
        if game.level > 6:
            fps = 120
            v = 120
        clock.tick(fps)
        pygame.display.flip()


def final():
    screen = pygame.display.set_mode((START_WIDTH, START_HEIGHT))
    fon = pygame.transform.scale(game.load_image('digger_start.png'), (START_WIDTH, START_HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 100)
    clock = pygame.time.Clock()
    string_rendered = font.render("GAME OVER", 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 80
    intro_rect.x = 250
    screen.blit(string_rendered, intro_rect)
    font = pygame.font.Font(None, 70)
    string_rendered = font.render(game.status, 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 250
    intro_rect.x = (START_WIDTH - intro_rect.width) // 2
    screen.blit(string_rendered, intro_rect)

    string_rendered = font.render(f'Ваша награда: {game.score}$', 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 390
    intro_rect.x = (START_WIDTH - intro_rect.width) // 2
    screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(50)

main()
final()
pygame.quit()
