import pygame
import collections
import random
import os

SrfcClrStrtLen = collections.namedtuple('SrfcClrStrtLen', 'srfc clr strt len')


def rollover(current, maximum):
    if current < 0:
        current += maximum
    elif current >= maximum:
        current -= maximum
    return current


class PacMap:
    def __init__(self):
        pass

    def __init__(self, num_wide, num_high):

        # create empty array for every possible block of the map
        self.map = [[None for i in range(num_high)] for j in range(num_wide)]

        # create ghost 'house' and surrounding tiles
        self.map[int((num_wide - 1) / 2)][int((num_high + 1) / 2)] = MapBlock(False, True, True, False)
        self.map[int((num_wide - 1) / 2) - 1][int((num_high + 1) / 2)] = MapBlock(False, False, True, False)
        self.map[int((num_wide - 1) / 2) - 2][int((num_high + 1) / 2)] = MapBlock(True, True, False, True)
        self.map[int((num_wide - 1) / 2) - 2][int((num_high + 1) / 2) - 1] = MapBlock(False, False, True, True)
        self.map[int((num_wide - 1) / 2) - 2][int((num_high + 1) / 2) + 1] = MapBlock(True, False, True, False)
        next_block_to_add = []
        for i in range(int((num_wide - 1) / 2) - 2):
            if i == 0 or self.map[i-1][int((num_high + 1) / 2)].up:
                self.map[i][int((num_high + 1) / 2)] = MapBlock(False, True, True, False)
            else:
                rand_bool = random.choice([True, False])
                self.map[i][int((num_high + 1) / 2)] = MapBlock(rand_bool, True, True, rand_bool)
                if rand_bool:
                    next_block_to_add.append((i, int((num_high + 1) / 2) - 1))
                    next_block_to_add.append((i, int((num_high + 1) / 2) + 1))

        # create tiles based on number of cols
        self.map[int((num_wide - 1) / 2)][int((num_high + 1) / 2) - 1] = \
            MapBlock(num_wide % 2 == 1, True, True, False)
        self.map[int((num_wide - 1) / 2) - 1][int((num_high + 1) / 2) - 1] = \
            MapBlock(num_wide % 2 != 1, True, True, False)
        self.map[int((num_wide - 1) / 2)][int((num_high + 1) / 2) + 1] = \
            MapBlock(False, True, True, num_wide % 2 == 1)
        self.map[int((num_wide - 1) / 2) - 1][int((num_high + 1) / 2) + 1] = \
            MapBlock(False, True, True, num_wide % 2 != 1)
        for i in range(num_high):
            if not self.map[int((num_wide - 1) / 2) - 1 + (num_wide % 2)][i]:
                if i == 0 or self.map[int((num_wide - 1) / 2) - 1 + (num_wide % 2)][i-1].left:
                    self.map[int((num_wide - 1) / 2) - 1 + (num_wide % 2)][i] = \
                        MapBlock(True, False, False, True)
                else:
                    rand_bool = random.choice([True, True, False])
                    self.map[int((num_wide - 1) / 2) - 1 + (num_wide % 2)][i] = \
                        MapBlock(True, rand_bool, rand_bool, True)
                    if rand_bool:
                        next_block_to_add.append((int((num_wide - 1) / 2) - 2 + (num_wide % 2), i))
                        if num_wide % 2 == 0:
                            next_block_to_add.append((int((num_wide - 1) / 2) + (num_wide % 2), i))

        # create the left side of the map
        while len(next_block_to_add) > 0:
            current = next_block_to_add[0]
            col = int(current[0])
            row = int(current[1])
            if not self.map[col][row]:
                if self.map[col][rollover(row-1, num_high)]:
                    up = self.map[col][rollover(row-1, num_high)].down
                elif row == 0:
                    up = False
                else:
                    up = random.choice([True, True, False])
                    if up:
                        next_block_to_add.append((col, rollover(row-1, num_high)))
                if self.map[col][rollover(row+1, num_high)]:
                    down = self.map[col][rollover(row+1, num_high)].up
                elif row == num_high-1:
                    down = False
                else:
                    down = random.choice([True, True, False])
                    if down:
                        next_block_to_add.append((col, rollover(row+1, num_high)))
                if self.map[rollover(col-1, num_wide)][row]:
                    left = self.map[rollover(col-1, num_wide)][row].right
                elif col == 0:
                    left = False
                else:
                    left = random.choice([True, True, False])
                    if left and (rollover(col-1, num_wide) < col):
                        next_block_to_add.append((rollover(col-1, num_wide), row))
                if self.map[rollover(col+1, num_wide)][row]:
                    right = self.map[rollover(col+1, num_wide)][row].left
                else:
                    right = random.choice([True, True, False])
                    if right and col+1 <= int((num_wide - 1) / 2):
                        next_block_to_add.append((rollover(col+1, num_wide), row))

                self.map[col][row] = MapBlock(up, left, right, down)
                # print('MapBlock created at ({}, {}) with attributes up={}, left={}, right={}, down={}'.format(
                #              col, row, up, left, right, down))
            next_block_to_add.remove(current)

        for i in range(int((num_wide - 1) / 2)+1):
            for j in range(num_high):
                if self.map[i][j]:
                    self.map[num_wide-i-1][j] = MapBlock(self.map[i][j].up,
                                                         self.map[i][j].right,
                                                         self.map[i][j].left,
                                                         self.map[i][j].down)


class MapBlock:
    def __init__(self, arg1, arg2, arg3, arg4):
        self.up = arg1
        self.left = arg2
        self.right = arg3
        self.down = arg4

    def draw_block(self, line_info):
        if not self.up:
            end = (line_info.strt[0]+line_info.len, line_info.strt[1])
            pygame.draw.line(line_info.srfc, line_info.clr, line_info.strt, end, 1)
        if not self.left:
            end = (line_info.strt[0], line_info.strt[1] + line_info.len)
            pygame.draw.line(line_info.srfc, line_info.clr, line_info.strt, end, 1)
        if not self.right:
            start = (line_info.strt[0] + line_info.len, line_info.strt[1])
            end = (start[0], start[1] + line_info.len)
            pygame.draw.line(line_info.srfc, line_info.clr, start, end, 1)
        if not self.down:
            start = (line_info.strt[0], line_info.strt[1] + line_info.len)
            end = (start[0] + line_info.len, start[1])
            pygame.draw.line(line_info.srfc, line_info.clr, start, end, 1)

    def check_dir(self, dir):
        if dir == "UP":
            return self.up
        elif dir == "LEFT":
            return self.left
        elif dir == "RIGHT":
            return self.right
        elif dir == "DOWN":
            return self.down
        return False


class Pacman(pygame.sprite.Sprite):
    moving_dir = 0
    next_dir = 0
    centre_x = None
    centre_y = None
    death = []
    move_up = []
    move_left = []
    move_right = []
    move_down = []

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        for i in range(12):
            if i < 2:
                self.move_up.append(pygame.image.load(os.path.abspath(
                    os.path.join('.', 'PacmanPics\Move\PacUp{}.jpg'.format(i + 1)))))
                self.move_left.append(pygame.image.load(os.path.abspath(
                    os.path.join('.', 'PacmanPics\Move\PacLeft{}.jpg'.format(i + 1)))))
                self.move_right.append(pygame.image.load(os.path.abspath(
                    os.path.join('.', 'PacmanPics\Move\PacRight{}.jpg'.format(i + 1)))))
                self.move_down.append(pygame.image.load(os.path.abspath(
                    os.path.join('.', 'PacmanPics\Move\PacDown{}.jpg'.format(i + 1)))))
            self.death.append(pygame.image.load(os.path.abspath(
                    os.path.join('.', 'PacmanPics\Death\PacDeath{}.jpg'.format(i + 1)))))
        self.death[0] = pygame.image.load(os.path.abspath(
                    os.path.join('.', 'PacmanPics\Death\PacDeath1.png'))).convert_alpha()
        self.image = self.death[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.centre_x = self.rect.center[0]
        self.centre_y = self.rect.center[1]

    def turn(self, mr_map, tile_size):
        if self.moving_dir == 0 and \
                mr_map.map[int(self.rect.x / tile_size)][int(self.rect.y / tile_size)].check_dir(self.next_dir):
            self.moving_dir = self.next_dir
        elif (self.moving_dir == 'UP' or self.moving_dir == 'DOWN') and self.rect.y % tile_size == 2:
            if mr_map.map[int(self.rect.x / tile_size)][int(self.rect.y / tile_size)].check_dir(self.next_dir):
                self.moving_dir = self.next_dir
            elif mr_map.map[int(self.rect.x / tile_size)][int(self.rect.y / tile_size)].check_dir(self.moving_dir):
                pass
            else:
                self.moving_dir = 0
        elif (self.moving_dir == 'RIGHT' or self.moving_dir == 'LEFT') and self.rect.x % tile_size == 2:
            if mr_map.map[int(self.rect.x / tile_size)][int(self.rect.y / tile_size)].check_dir(self.next_dir):
                self.moving_dir = self.next_dir
            elif mr_map.map[int(self.rect.x / tile_size)][int(self.rect.y / tile_size)].check_dir(self.moving_dir):
                pass
            else:
                self.moving_dir = 0

    def move(self, max_w, max_h):
        if self.moving_dir == 'UP':
            if self.image == self.move_up[0]:
                self.image = self.move_up[1]
            else:
                self.image = self.move_up[0]
            self.rect.y = rollover(self.rect.y + 4, max_h) - 5
        if self.moving_dir == 'DOWN':
            if self.image == self.move_down[0]:
                self.image = self.move_down[1]
            else:
                self.image = self.move_down[0]
            self.rect.y = rollover(self.rect.y + 6, max_h) - 5
        if self.moving_dir == 'LEFT':
            if self.image == self.move_left[0]:
                self.image = self.move_left[1]
            else:
                self.image = self.move_left[0]
            self.rect.x = rollover(self.rect.x + 4, max_w) - 5
        if self.moving_dir == 'RIGHT':
            if self.image == self.move_right[0]:
                self.image = self.move_right[1]
            else:
                self.image = self.move_right[0]
            self.rect.x = rollover(self.rect.x + 6, max_w) - 5


class Ghost(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Blinky(Ghost):
    moving_dir = 0
    next_dir = 0
    rect = None
    x = None
    y = None
    centre_x = 0
    centre_y = 0
    death = []
    move_up = []
    move_left = []
    move_right = []
    move_down = []
    current_img = None
    sprite_mask = None

    def __init__(self):
        Ghost.__init__(self)
        for i in range(2):
            self.move_up.append(pygame.image.load(os.path.abspath(
                os.path.join('.', 'GhostPics\Blinky\BlinkyUp{}.png'.format(i + 1)))))
            self.move_left.append(pygame.image.load(os.path.abspath(
                os.path.join('.', 'GhostPics\Blinky\BlinkyLeft{}.png'.format(i + 1)))))
            self.move_right.append(pygame.image.load(os.path.abspath(
                os.path.join('.', 'GhostPics\Blinky\BlinkyRight{}.png'.format(i + 1)))))
            self.move_down.append(pygame.image.load(os.path.abspath(
                    os.path.join('.', 'GhostPics\Blinky\BlinkyDown{}.png'.format(i + 1)))))
        self.current_img = self.move_down[0]
        self.sprite_mask = pygame.mask.from_surface(self.current_img)
        self.rect = self.current_img.get_rect()
        self.centre_x = self.rect.center[0]
        self.centre_y = self.rect.center[1]


class Pinky(Ghost):
    pass


class Inky(Ghost):
    pass


class Clyde(Ghost):
    pass


class Pellet(pygame.sprite.Sprite):

    def __init__(self, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((2, 2))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.mask = pygame.mask.from_surface(self.image)
