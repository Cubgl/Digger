import pygame

from Classes.Game import GameDigger


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
            key = pygame.key.get_pressed()
            if key[pygame.K_DOWN]:
                if game.player.may_be_down(game):
                    game.player.image = game.player_image['down']
                    game.player.go_down(game)
            elif key[pygame.K_UP]:
                if game.player.may_be_up(game):
                    game.player.image = game.player_image['up']
                    game.player.go_up(game)
            elif key[pygame.K_RIGHT]:
                if game.player.may_be_right(game):
                    game.player.image = game.player_image['right']
                    game.player.go_right(game)
            elif key[pygame.K_LEFT]:
                if game.player.may_be_left(game):
                    game.player.image = game.player_image['left']
                    game.player.go_left(game)
        screen[game.level].fill((0, 0, 0))
        game.all_sprites.draw(screen[game.level])
        pygame.display.set_caption(f'Score = {game.score}, Level = {game.level}')
        for sack in game.sack_group.sprites():
            sack.fall(game, v / fps)
        if pygame.sprite.spritecollideany(game.player, game.monster_group) is not None:
            game.is_over = True
        if pygame.sprite.spritecollideany(game.player, game.finish_group) is not None:
            game.goto_next_level(screen[game.level])
            if not game.is_over:
                size = game.width_canvas, game.height_canvas
                screen[game.level] = pygame.display.set_mode(size)
        if game.is_over:
            running = False
        clock.tick(fps)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    game = GameDigger()
    size = game.width_canvas, game.height_canvas
    screen = [None] * (game.count_levels + 1)
    screen[game.level] = pygame.display.set_mode(size)
    main()
    pygame.quit()
