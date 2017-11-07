from random import *

import pygame

from abstract_state import AbstractState
from src.constants import *
from src.fairy_powers.power_manager import PowerManager
from src.map.map_automata import MapAutomata
from src.map.map_generator import MapGenerator
from src.map.map_image import MapImage
from src.map.path_finding_map import PathFindingMap
from src.map.plant_map import PlantMap
from src.map.river_generator import RiverGenerator
from src.state.state_components.object_creator import ObjectCreator
from src.ui.ui import UI
from state_components.ai_handler import AIHandler
from state_components.cursor import Cursor
from state_components.draw_list import DrawList
from state_components.effect_handler import EffectHandler
from state_components.mouse_handler import MouseHandler
from state_components.mushlock_ai_overlord import MushlockAIOverlord
from state_components.object_list import ObjectList
from state_components.score_keeper import ScoreKeeper
from state_components.shroud import Shroud
from state_components.turn_tracker import TurnTracker
from state_components.view import View
from src.map.decay_map import DecayMap


class GameState(AbstractState):

    AI_SPEED = AI_SPEED
    NUM_ORCS = 10
    ORC_RATE = 50

    shot_count = 0

    def __init__(self, state_manager):

        self.power_manager = PowerManager(self)
        AbstractState.__init__(self, state_manager)

        self.frame = 0

        self.terrain_map = MapGenerator.generate_cave_map()
        self.terrain_map.bind_state(self)
        self.plant_map = PlantMap(self)
        self.decay_map = DecayMap(self)
        self.map_image = MapImage(self.terrain_map, self)
        self.path_finding_map = PathFindingMap(self, self.terrain_map)
        self.mushlock_ai_overlord = MushlockAIOverlord(self)
        self.score_keeper = ScoreKeeper(self)
        self.cursor = Cursor(self)

        self.turn_tracker = TurnTracker(self)

        self.view = View(self.map_image)
        self.mouse_handler = MouseHandler(self)

        self.effect_handler = EffectHandler(self)
        self.object_list = ObjectList(self)
        self.draw_list = DrawList(self)
        self.object_creator = ObjectCreator(self)
        self.ai_handler = AIHandler(self)

        self.shroud = Shroud(self)

        self.river_generator = RiverGenerator(self, self.terrain_map)
        self.map_automata = MapAutomata(self, self.terrain_map)

        self.ONE_POWER_PER_TURN_MODE = True
        self.end_turn_flag = False
        self.over_flag = False

        self.orc_timer = 0
        self.orc_band_size = 2

        self.initialize()

    def initialize(self):

        self.map_automata.initial_automata()
        self.place_gems()
        self.path_finding_map.compute()

        self.spawn_orcs(GameState.NUM_ORCS)

    def initialize_ui(self):

        return UI.create_game_ui(self)

    def handle_input(self):

        # returns true to exit game
        for event in pygame.event.get():

            if event.type == QUIT:
                self.trigger_exit()

            elif event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    self.open_in_game_menu()

                elif event.key == UP:
                    self.view.press('up')
                elif event.key == DOWN:
                    self.view.press('down')
                elif event.key == RIGHT:
                    self.view.press('right')
                elif event.key == LEFT:
                    self.view.press('left')

                # TODO this is a cheat
                # elif event.key == K_r:
                #     self.reveal_map()

                elif event.key == K_x:
                    self.take_screen_shot()
                elif event.key == K_SLASH:
                    self.toggle_fullscreen()

                # blocked by ai turn

                if self.turn_tracker.fairy_turn:
                    if event.key == K_SPACE:
                        self.end_player_turn()

            elif event.type == KEYUP:
                if event.key == UP:
                    self.view.release('up')
                elif event.key == DOWN:
                    self.view.release('down')
                elif event.key == RIGHT:
                    self.view.release('right')
                elif event.key == LEFT:
                    self.view.release('left')

            elif event.type == MOUSEBUTTONDOWN:

                # blocked by ai turn

                if self.turn_tracker.fairy_turn:
                    if event.button == 1:
                        self.mouse_handler.left_click()

            elif event.type == MOUSEMOTION:

                self.cursor.update()

    def trigger_exit(self):
        self.exit_state = True

    def run(self):

        self.ui.run()
        self.view.run()
        self.object_list.run()
        self.effect_handler.run()

        if self.turn_tracker.ai_turn and self.is_ai_frame():
            self.ai_handler.run()

        if not self.effect_handler.effects and self.end_turn_flag:
            self.end_turn_flag = False
            self.end_player_turn()

    def draw(self):
        self.map_image.draw(self.screen)
        self.plant_map.draw(self.screen)
        self.draw_list.draw(self.screen)
        self.effect_handler.draw(self.screen)

        self.cursor.draw(self.screen)
        self.ui.draw(self.screen)

    def end_player_turn(self):
        self.decay_map.run()
        self.map_automata.run()
        self.check_for_starvation()
        self.spawn_new_mushlocks()
        self.turn_tracker.end_turn()
        self.mushlock_ai_overlord.update_ai_state()
        self.run_orc_spawner()

        self.score_keeper.add_turn()

        self.check_for_end_state()

    def check_for_starvation(self):
        mushlocks = self.object_list.get_all('mushlock')
        for mush in mushlocks:
            mush.ai_component.starve()

    def spawn_new_mushlocks(self):
        houses = self.object_list.get_all('mushhouse')
        for house in houses:
            house.run_house()

    def reveal_map(self):
        self.map_image.reveal_all()
        self.shroud.explore_all()

    def is_ai_frame(self):

        self.frame += 1
        if self.frame % GameState.AI_SPEED == 0:
            self.frame = 0
            return True
        return False

    def take_screen_shot(self):
        pygame.image.save(self.screen, ''.join(('screen', str(GameState.shot_count), '.png')))
        GameState.shot_count += 1

    def start_of_turn(self):

        self.object_creator.spawn_new_houses()

    def place_gems(self):

        hidden_gems = MapGenerator.place_hidden_gems(self.terrain_map)
        revealed_gems = MapGenerator.place_revealed_gems(self.terrain_map)

        gems = hidden_gems + revealed_gems
        map(self.object_creator.add_gem, gems)

    def spawn_orcs(self, num):

        def point_not_too_close_to_start(self, point):
            min_dist = 50
            prox = self.path_finding_map.return_map.get(point, None)
            return prox is None or prox > min_dist

        free = filter(lambda x: not self.object_list.point_is_blocked(x) and point_not_too_close_to_start(self, x),
                      self.terrain_map.get_all((FLOOR, GROWTH_1)))
        if num < len(free):

            points = sample(free, num)

            for point in points:
                self.object_creator.add_orc(point)

    def run_orc_spawner(self):

        self.orc_timer += choice((1, 1, 1, 2))
        if self.orc_timer >= GameState.ORC_RATE:
            self.orc_timer = 0
            count = len(self.object_list.get_all('orc'))
            if count + self.orc_band_size < MAX_ORCS:
                self.spawn_orcs(self.orc_band_size)
                self.orc_band_size += randint(1, 2)

    def check_for_end_state(self):

        if self.over_flag:
            self.game_over()
        if len(self.object_list.get_all(('mushlock', 'mushhouse'))) < 1:
            self.over_flag = True

    def game_over(self):

        next_state = self.state_manager.load_score_state(self, self.screen, fade=True)
        self.set_next_state(next_state)
        self.trigger_exit()

    def flag_end_turn(self):
        self.end_turn_flag = True

    def open_in_game_menu(self):
        self.set_next_state(self.state_manager.load_in_game_menu(self, self.screen))
        self.trigger_exit()

