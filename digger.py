import pygame

from Classes.Game import GameDigger


def main():
    running = True
    v = 60
    fps = 60
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            key = pygame.key.get_pressed()
            if key[pygame.K_DOWN]:
                if game.player.may_be_down(game):
                    game.player.go_down(game)
            elif key[pygame.K_UP]:
                if game.player.may_be_up(game):
                    game.player.go_up(game)
            if key[pygame.K_RIGHT]:
                if game.player.may_be_right(game):
                    game.player.go_right(game)
            elif key[pygame.K_LEFT]:
                if game.player.may_be_left(game):
                    game.player.go_left(game)
        screen.fill((0, 0, 0))
        game.all_sprites.draw(screen)
        for sack in game.sack_group.sprites():
            print(f'Sack: {sack.pos_y}, {sack.pos_x}')
            sack.fall(game, v / fps)
        clock.tick(fps)
        pygame.display.set_caption(f'Score = {game.score}')
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    game = GameDigger()
    size = width, height = game.width_canvas, game.height_canvas
    screen = pygame.display.set_mode(size)
    main()
    pygame.quit()
