import pygame
import PacMap
import random
import PacMethods


def main():
    # start pygame modules that need to be started
    pygame.init()

    tile_size = 20

    # display setting information
    display_w = (14*tile_size)+1
    display_h = (17*tile_size)+1

    # store RGB colour codes for pygame in tuples
    rgb_black = (0, 0, 0)
    rgb_white = (255, 255, 255)
    rgb_red = (255, 0, 0)
    rgb_green = (0, 255, 0)
    rgb_blue = (0, 0, 255)
    colour_codes = [rgb_red, rgb_white, rgb_green, rgb_blue]

    # create the window with caption and a game clock
    game_window = pygame.display.set_mode((display_w, display_h))
    pygame.display.set_caption('Python Pacman')
    clock = pygame.time.Clock()

    num_tiles_high = int(display_h/tile_size)
    num_tiles_wide = int(display_w/tile_size)

    # create map and pellets
    mr_map = PacMap.PacMap(num_tiles_wide, num_tiles_high)
    pellet_list = PacMethods.create_pellets(mr_map, tile_size)

    # create PacMan and place him in an active tile
    hero = PacMap.Pacman()
    index = 0
    while not mr_map.map[0][index]:
        index += 1
    hero.rect.x = int(tile_size/2) - hero.centre_x
    hero.rect.y = index*tile_size + int(tile_size/2) - hero.centre_y

    # create Blinky and place him above the jail
    blinky = PacMap.Blinky()
    blinky.x = int(num_tiles_wide/2)*tile_size + int(tile_size/2) - blinky.centre_x
    blinky.y = int((num_tiles_high-1)/2)*tile_size + int(tile_size/2) - blinky.centre_y

    animation_tracker = 0

    # start the game loop
    continue_game = True
    while continue_game:
        animation_tracker += 1

        # pygame event loop stacks events in a frame
        continue_game = event_loop(continue_game, hero)
        # turning Pacman
        hero.turn(mr_map, tile_size)
        # moving Pacman
        hero.move(display_w, display_h)
        # calculate ghost paths

        # move the ghosts

        # test collisions
        for pellet in pygame.sprite.spritecollide(hero, pellet_list, True):
            print('collected pellet at ({}, {})'.format(pellet.rect.x, pellet.rect.y))
        if hero.mask.overlap(blinky.sprite_mask, (hero.rect.x - blinky.x, hero.rect.y - blinky.y)):
            print('Oh no!')

        # every 3 ticks execute drawing commands
        if animation_tracker % 3 == 0:
            # draw the background then tiles
            game_window.fill(rgb_black)
            for i in range(num_tiles_wide):
                for j in range(num_tiles_high):
                    if mr_map.map[i][j]:
                        draw_info = PacMap.SrfcClrStrtLen(game_window, random.choice(colour_codes),
                                                      (i*tile_size, j*tile_size), tile_size)
                        mr_map.map[i][j].draw_block(draw_info)
                    else:
                        pygame.draw.rect(game_window, random.choice(colour_codes),
                                     (i*tile_size+1, j*tile_size+1, tile_size-1, tile_size-1), 0)

            # draw/blit the game objects
            pellet_list.draw(game_window)
            game_window.blit(hero.image, (hero.rect.x, hero.rect.y))
            game_window.blit(blinky.current_img, (blinky.x, blinky.y))
            # after drawing update to the screen
            pygame.display.update()
        # clock frames updated
        clock.tick(50)

    pygame.quit()
    quit()


def event_loop(continue_game, hero):
    for event in pygame.event.get():
        # activates if user closes game window
        if event.type == pygame.QUIT:
            continue_game = False
        # activates on click
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                hero.next_dir = 'UP'
                if hero.moving_dir == 'DOWN':
                    hero.moving_dir = 'UP'
            elif event.key == pygame.K_LEFT:
                hero.next_dir = 'LEFT'
                if hero.moving_dir == 'RIGHT':
                    hero.moving_dir = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                hero.next_dir = 'RIGHT'
                if hero.moving_dir == 'LEFT':
                    hero.moving_dir = 'RIGHT'
            elif event.key == pygame.K_DOWN:
                hero.next_dir = 'DOWN'
                if hero.moving_dir == 'UP':
                    hero.moving_dir = 'DOWN'
    return continue_game


if __name__ == '__main__':
    main()
