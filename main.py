import arcade
import math

from arcade import SpriteList
from const import ENEMIES, TOWERS, MAP_POINTS
from objects import EnemyEnum, Tower
from gui import GUI

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 786
class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Tower Defense Game")
        self.background = arcade.load_texture("media/map.png")
        self.temporary_enemy_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.tower_list = arcade.SpriteList()
        self.mouse_x = 0
        self.mouse_y = 0
        self.gold = 200

        self.target_points = None
        self.enemies_to_create = None
        self.enemies_start_point = None
        self.enemy_spawn = None
        self.enemy_spawn_timer = 0

        self.gui = GUI(self)
        self.setup()
        self.setup_enemies()

    def setup(self):
        self.load_font()

    def setup_enemies(self):
        self.target_points = MAP_POINTS["MAP_1"]["points"]
        self.enemies_to_create = MAP_POINTS["MAP_1"]["enemies"]
        self.enemies_start_point = MAP_POINTS["MAP_1"]["enemies_start_point"]
        self.enemy_spawn = MAP_POINTS["MAP_1"]["enemy_spawn"]
        self.create_enemies()

    def reset_spawn_timer(self):
        self.enemy_spawn_timer = self.enemy_spawn

    @staticmethod
    def load_font():
        arcade.load_font("media/GODOFWAR.TTF")

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        point = (x, y)
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.gui.dragged_element = None

        if not self.gui.dragged_element:
            self.gui.process_item_at_point(point)
        else:
            self.gui.buy_tower()

    def create_enemies(self):
        for enemy_type, amount in self.enemies_to_create.items():
            for _ in range(amount):
                enemy = self.create_enemy(EnemyEnum[enemy_type].value)
                self.temporary_enemy_list.append(enemy)

    def create_enemy(self, enemy):
        _enemy = enemy(*self.enemies_start_point, self.target_points.copy())
        return _enemy

    def spawn_enemies(self, delta_time: float):
        # Spawn enemy one by one every self.enemy_spawn seconds
        if len(self.temporary_enemy_list) <= 0:
            return
        self.enemy_spawn_timer -= delta_time
        if self.enemy_spawn_timer <= 0:
            enemy = self.temporary_enemy_list.pop(0)
            enemy.change_state("moving")
            self.enemy_list.append(enemy)
            self.reset_spawn_timer()

    def towers_target_enemy(self):
        for tower in self.tower_list:
            tower.aim_enemy(self.enemy_list)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, 1024, 786, self.background)
        for enemy in self.enemy_list:
            enemy.draw()
        for tower in self.tower_list:
            tower.draw()

        self.gui.draw()

    def on_update(self, delta_time: float):
        self.spawn_enemies(delta_time)
        self.towers_target_enemy()
        self.enemy_list.update()
        self.tower_list.update()
        self.gui.update()


def main():
    window = GameWindow()
    arcade.run()

if __name__ == "__main__":
    main()
