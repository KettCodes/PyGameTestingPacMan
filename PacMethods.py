import PacMap
import pygame


def create_pellets(maze, tile_width):
    list = pygame.sprite.Group()

    for i in range(len(maze.map)):
        for j in range(len(maze.map[i])):
            if maze.map[i][j]:
                if j != int((len(maze.map[i]) + 1) / 2) or abs(i - (len(maze.map) - 1) / 2) >= 2:
                    list.add(PacMap.Pellet(i * tile_width + int(tile_width / 2),
                                           j * tile_width + int(tile_width / 2)))
                    if maze.map[i][j].down and j < len(maze.map[i]) - 1:
                        list.add(
                            PacMap.Pellet(i * tile_width + int(tile_width / 2), (j + 1) * tile_width))
                    if maze.map[i][j].right and i < len(maze.map) - 1:
                        list.add(
                            PacMap.Pellet((i + 1) * tile_width, j * tile_width + int(tile_width / 2)))

    return list
