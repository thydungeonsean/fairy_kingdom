import pygame
import os
import sys
from constants import *
from state.state_manager import StateManager


def initialize_display():

    pygame.init()

    pygame.display.set_mode((SCREENW, SCREENH))
    # pygame.display.set_mode((SCREENW, SCREENH), FULLSCREEN)
    os.environ['SDL_VIDEO_CENTERED'] = "TRUE"

    pygame.display.set_caption('Fairy Kingdom')


def main():

    initialize_display()

    game = StateManager()
    game.main()

    sys.exit()
