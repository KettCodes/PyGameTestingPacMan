import pygame
import PacMap
import random


def main():
    # start pygame modules that need to be started
    pygame.init()

    tile_size = 20

    # display setting information
    display_w = (42*tile_size)+1
    display_h = (31*tile_size)+1

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

    MrMap = PacMap.PacMap(num_tiles_wide, num_tiles_high)
    hero = PacMap.Pacman()
    index = 0
    while not MrMap.map[0][index]:
        index += 1
    hero.y = index*tile_size + 2

    animation_tracker = 0

    # start the game loop
    continue_game = True
    while continue_game:
        animation_tracker += 1

        # pygame event loop stacks events in a frame
        for event in pygame.event.get():
            # activates if user closes game window
            if event.type == pygame.QUIT:
                continue_game = False
            # activates on click
            if event.type == pygame.KEYDOWN:
                # print('{} was pressed'.format(pygame.key.name(event.key)))
                current_key = pygame.key.name(event.key)
                if current_key == 'up':
                    hero.next_dir = 'UP'
                    if hero.moving_dir == 'DOWN':
                        hero.moving_dir = 'UP'
                elif current_key == 'left':
                    hero.next_dir = 'LEFT'
                    if hero.moving_dir == 'RIGHT':
                        hero.moving_dir = 'LEFT'
                elif current_key == 'right':
                    hero.next_dir = 'RIGHT'
                    if hero.moving_dir == 'LEFT':
                        hero.moving_dir = 'RIGHT'
                elif current_key == 'down':
                    hero.next_dir = 'DOWN'
                    if hero.moving_dir == 'UP':
                        hero.moving_dir = 'DOWN'
                # print('the next dir is: {}'.format(hero.next_dir))

        # turning Pacman
        if hero.moving_dir == 0 and \
                MrMap.map[int(hero.x/tile_size)][int(hero.y/tile_size)].check_dir(hero.next_dir):
            hero.moving_dir = hero.next_dir

        elif (hero.moving_dir == 'UP' or hero.moving_dir == 'DOWN') and hero.y % tile_size == 2:
            if MrMap.map[int(hero.x / tile_size)][int(hero.y / tile_size)].check_dir(hero.next_dir):
                hero.moving_dir = hero.next_dir
            elif MrMap.map[int(hero.x/tile_size)][int(hero.y/tile_size)].check_dir(hero.moving_dir):
                pass
            else:
                hero.moving_dir = 0

        elif (hero.moving_dir == 'RIGHT' or hero.moving_dir == 'LEFT') and hero.x % tile_size == 2:
            if MrMap.map[int(hero.x / tile_size)][int(hero.y / tile_size)].check_dir(hero.next_dir):
                hero.moving_dir = hero.next_dir
            elif MrMap.map[int(hero.x/tile_size)][int(hero.y/tile_size)].check_dir(hero.moving_dir):
                pass
            else:
                hero.moving_dir = 0

        # moving Pacman
        if hero.moving_dir == 'UP':
            if hero.current_img == hero.move_up[0]:
                hero.current_img = hero.move_up[1]
            else:
                hero.current_img = hero.move_up[0]
            hero.y = PacMap.rollover(hero.y + 4, display_h) - 5
        if hero.moving_dir == 'DOWN':
            if hero.current_img == hero.move_down[0]:
                hero.current_img = hero.move_down[1]
            else:
                hero.current_img = hero.move_down[0]
            hero.y = PacMap.rollover(hero.y + 6, display_h) - 5
        if hero.moving_dir == 'LEFT':
            if hero.current_img == hero.move_left[0]:
                hero.current_img = hero.move_left[1]
            else:
                hero.current_img = hero.move_left[0]
            hero.x = PacMap.rollover(hero.x + 4, display_w) - 5
        if hero.moving_dir == 'RIGHT':
            if hero.current_img == hero.move_right[0]:
                hero.current_img = hero.move_right[1]
            else:
                hero.current_img = hero.move_right[0]
            hero.x = PacMap.rollover(hero.x + 6, display_w) - 5

        # starting with the background the chessboard is drawn along with the active piece paths
        game_window.fill(rgb_black)

        for i in range(num_tiles_wide):
            for j in range(num_tiles_high):
                if MrMap.map[i][j]:
                    draw_info = PacMap.SrfcClrStrtLen(game_window, random.choice(colour_codes),
                                                      (i*tile_size, j*tile_size), tile_size)
                    MrMap.map[i][j].draw_block(draw_info)
                else:
                    pygame.draw.rect(game_window, random.choice(colour_codes),
                                     (i*tile_size+1, j*tile_size+1, tile_size-1, tile_size-1), 0)

        game_window.blit(hero.current_img, (hero.x, hero.y))

        # after drawing update to the screen and clock frames are updated
        if animation_tracker % 3 == 0:
            pygame.display.update()
        clock.tick(50)

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()

# current_key = pygame.key.get_pressed()

# if current_key[pygame.K_LEFT]:
#    hero.col -= x_change
# if current_key[pygame.K_RIGHT]:
#    hero.col += x_change