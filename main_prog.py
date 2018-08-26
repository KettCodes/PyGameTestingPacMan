import pygame
import PacMap
import random
import PacMethods


def main():
    # start pygame modules that need to be started
    pygame.init()

    tile_size = 20

    # display setting information
    display_w = (25*tile_size)+1
    display_h = (22*tile_size)+1

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

    # create Blinky and place him above the ghost house
    blinky = PacMap.Blinky()
    blinky.rect.x = int(num_tiles_wide/2)*tile_size + int(tile_size/2) - blinky.centre_x
    blinky.rect.y = int((num_tiles_high-1)/2)*tile_size + int(tile_size/2) - blinky.centre_y
    blinky.scatter_target = (num_tiles_wide - 1, index)

    # create Pinky and place him in the ghost house
    pinky = PacMap.Pinky()
    pinky.rect.x = int(num_tiles_wide/2)*tile_size + int(tile_size/2) - pinky.centre_x
    pinky.rect.y = (int((num_tiles_high-1)/2) + 1)*tile_size + int(tile_size/2) - pinky.centre_y
    pinky.scatter_target = (0, index)

    # set new index
    index = num_tiles_high - 1
    while not mr_map.map[0][index]:
        index -= 1

    # create Inky and place him in the ghost house
    inky = PacMap.Inky()
    inky.rect.x = (int(num_tiles_wide / 2) - 1) * tile_size + int(tile_size / 2) - inky.centre_x
    inky.rect.y = (int((num_tiles_high - 1) / 2) + 1) * tile_size + int(tile_size / 2) - inky.centre_y
    inky.scatter_target = (num_tiles_wide - 1, index)

    # setup ghost groups
    active_ghosts = pygame.sprite.Group()
    passive_ghosts = pygame.sprite.Group()
    active_ghosts.add(blinky)
    passive_ghosts.add(pinky)
    passive_ghosts.add(inky)

    # start the game loop
    animation_tracker = 0
    continue_game = True
    while continue_game:
        animation_tracker += 1

        # pygame event loop stacks events in a frame
        continue_game = event_loop(continue_game, hero)
        # turning Pacman
        hero.turn(mr_map, tile_size)
        # moving Pacman
        hero.move(display_w, display_h)
        # move the ghosts
        if animation_tracker%750 == 0:
            for ghost in active_ghosts:
                ghost.mode = "SCATTER"
        elif (animation_tracker-150)%750 == 0:
            for ghost in active_ghosts:
                ghost.mode = "CHASE"

        for ghost in active_ghosts:
            ghost.move(mr_map, tile_size, hero)
        for ghost in passive_ghosts:
            ghost.patience()
        if animation_tracker == 500:
            pinky.rect.y -= tile_size
            active_ghosts.add(pinky)
            passive_ghosts.remove(pinky)
        if animation_tracker == 1000:
            inky.rect.y -= tile_size
            active_ghosts.add(inky)
            passive_ghosts.remove(inky)

        # test collisions
        for pellet in pygame.sprite.spritecollide(hero, pellet_list, True):
            print('collected pellet at ({}, {})'.format(pellet.rect.x, pellet.rect.y))
        for ghost in pygame.sprite.spritecollide(hero, active_ghosts, False, pygame.sprite.collide_mask):
            print('Oh no! You have been caught by {}'.format(ghost.__class__.__name__))

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
            game_window.blit(blinky.image, (blinky.rect.x, blinky.rect.y))
            game_window.blit(pinky.image, (pinky.rect.x, pinky.rect.y))
            game_window.blit(inky.image, (inky.rect.x, inky.rect.y))
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
