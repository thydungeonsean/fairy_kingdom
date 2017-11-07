from src.constants import *
import pygame


tiles = {
    HOR_WALL_1: (0, 0),
    HOR_WALL_2: (1, 0),
    HOR_WALL_3: (2, 0),
    WALL: (3, 0),
    SOLID_WALL: (3, 0),
    FLOOR: (4, 0),
    WATER_SOURCE: (7, 0),
    'water_a': (5, 0),
    'water_b': (6, 0),
    'water_source': (7, 0),
    PLANT: (0, 1),
    ROCK: (1, 1),
    GROWTH_1: (3, 1),
    GROWTH_2: (4, 1),
    GROWTH_3: (5, 1),
    'gem': (2, 1),
    'buried_gem': (6, 1),
    RUBBLE: (3, 3),

    # houses
    'mushhouse_l': (3, 2),
    'mushhouse_r': (4, 2),
    HOUSE_L: (3, 2),
    HOUSE_R: (4, 2),
    STUMP_L: (5, 2),
    STUMP_R: (6, 2),
    STUMP: (7, 2),

    # actors
    'mushlock_a': (0, 2),
    'mushlock_b': (1, 2),
    'mushlock_c': (2, 2),
    'orc_a': (0, 3),
    'orc_b': (1, 3),

    # powers
    'lure_a': (0, 4),
    'lure_b': (1, 4),
    'mark_a': (2, 4),
    'mark_b': (3, 4),

    # carried objects
    'food': (0, 5),
    'carried_gem': (1, 5),
    'empty_bucket': (2, 5),
    'full_bucket': (3, 5),
    'spear': (4, 5),
    'carried_spear': (5, 5),
    'pick': (6, 5),
    'carried_pick': (7, 5),

    'zzz_a': (0, 6),
    'zzz_b': (1, 6),

}


tile_sheet = None
tile_rect = pygame.Rect((0, 0), (TILEW, TILEH))


def load_tile_sheet():

    global tile_sheet

    if tile_sheet is None:
        tile_sheet = pygame.image.load('assets\\tiles.png').convert()

    return tile_sheet
