import pygame

from Classes.Game import GameDigger

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
            sack.fall(game, v / fps, True)
        for gold in game.gold_group.sprites():
            gold.fall(game, v / fps, False)
        if game.level > 3:
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
            print("Вас съел Монстр!")
            game.is_over = True
        if pygame.sprite.spritecollideany(game.player, game.finish_group,
                                          collided=pygame.sprite.collide_rect_ratio(
                                                  .75)) is not None:
            game.goto_next_level(screen[game.level])
            if not game.is_over:
                size = game.width_canvas, game.height_canvas
                screen[game.level] = pygame.display.set_mode(size)
        if game.is_over:
            running = False
        if game.level > 6:
            fps = 120
            v = 120
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
