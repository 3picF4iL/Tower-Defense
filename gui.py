import arcade
from arcade import SpriteList, Sprite
from objects import MiniTower, Tower
from const import ENEMIES, TOWERS

GOLD = 100


class Popup(arcade.Sprite):
    def __init__(self, x, y, y_shift=40, font_size=14, tower=None):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.texture = arcade.load_texture("media/details.png")
        self.scale = 0.5
        self.angle = 90

        self.y_shift = y_shift
        self.font_type = "GodOfWar"
        self.font_size = font_size
        self.alpha = 255
        self.text_shift = 25
        self.text_to_show = ""
        self.tower = tower
        self.setup()

    def setup(self):
        self.alpha = 200
        self.center_y = self.center_y + self.y_shift

    def draw_tower_info(self):
        if self.tower is not None:
            self.tower.show_range()
            self.tower.show_aimed_enemy()

    def draw_text(self):
        for i, text in enumerate(self.text_to_show):
            arcade.draw_text(text, self.center_x - 90, self.center_y + self.text_shift - (i * 20),
                             arcade.color.BLACK, self.font_size, font_name=self.font_type)

    def draw(self):
        self.draw_tower_info()
        super().draw()
        self.draw_text()

class GUI:
    def __init__(self, window):
        self.elements = SpriteList()
        self.dragged_element = None
        self.popups = []

        self.window = None
        self.SCREEN_WIDTH = 0
        self.SCREEN_HEIGHT = 0
        self.gold = 0

        # Initiate GUI settings
        self._initiate_gui(window)
        # Setup GUI
        self.setup_bottom_gui()
        self.setup_shop_gui()

    def _initiate_gui(self, window):
        self.window = window
        self.SCREEN_WIDTH = window.width
        self.SCREEN_HEIGHT = window.height
        self.gold = window.gold

    def setup_shop_gui(self):
        elements = [
            [self.SCREEN_WIDTH - 120, 30, 1],
            [self.SCREEN_WIDTH - 80, 30, 2],
            [self.SCREEN_WIDTH - 120, 70, 3],
            [self.SCREEN_WIDTH - 80, 70, 4]
        ]
        for element in elements:
            mini_tower = MiniTower(element[0], element[1], element[2])
            self.elements.append(mini_tower)

    def setup_bottom_gui(self):
        position = [self.SCREEN_WIDTH / 2, 50]
        bottom_gui = arcade.Sprite("media/details.png", 1, angle=90)
        bottom_gui.center_x = position[0]
        bottom_gui.center_y = position[1]
        bottom_gui.width = 100
        bottom_gui.height = self.SCREEN_WIDTH
        self.elements.append(bottom_gui)

    def setup_tower_popup(self, tower):
        if self.remove_tower_popup(tower):
            return
        text = [f"Type: {tower.tower_type}",
                f"Damage: {tower.damage}",
                f"Range: {tower.range}",
                f"Attack speed: {tower.attack_speed}"
                ]
        bg_sprite = Popup(tower.center_x, tower.center_y + 80, tower=tower)
        bg_sprite.text_to_show = text
        self.popups.append(bg_sprite)

    def remove_tower_popup(self, tower):
        for popup in self.popups:
            if popup.tower == tower:
                self.popups.remove(popup)
                return True
        return False

    def show_info(self):
        # Mouse position
        arcade.draw_text(f"Mouse position: {self.window.mouse_x}, {self.window.mouse_y}", 60, 70, arcade.color.BLACK, 15,
                         font_name="GodOfWar")
        # Enemies left
        arcade.draw_text(f"Enemies left: {len(self.window.enemy_list)}", 60, 50, arcade.color.BLACK, 15, font_name="GodOfWar")
        # Gold
        arcade.draw_text(f"Gold: {self.gold}", 60, 30, arcade.color.BLACK, 15, font_name="GodOfWar")

    def show_dragged_element(self):
        if self.dragged_element is None:
            return
        self.dragged_element.show_range()
        self.dragged_element.draw()

    def show_tower_popup(self):
        for popup in self.popups:
            popup.draw()

    def show_gui_elements(self):
        for element in self.elements:
            element.draw()

    def update_dragged_element(self):
        if self.dragged_element is None:
            return
        self.dragged_element.center_x = self.window.mouse_x
        self.dragged_element.center_y = self.window.mouse_y

    def set_dragged_element(self, element):
        print("Setting dragged element")
        if not element.disabled:
            self.dragged_element = Tower(element.center_x, element.center_y, element.tower_type)

    def process_item_at_point(self, point):
        temp_list = SpriteList()
        temp_list.extend(self.window.tower_list)
        temp_list.extend(self.elements)
        items = arcade.get_sprites_at_point(point, temp_list)
        print(f"Item at point: {items}")
        for item in items:
            if isinstance(item, MiniTower):
                self.set_dragged_element(item)
            elif isinstance(item, Tower):
                self.setup_tower_popup(tower=item)

    def modify_gold(self, value):
        self.gold += value

    def buy_tower(self):
        if self.dragged_element is not None:
            tower_cost = self.dragged_element.cost
            if self.gold >= tower_cost:
                self.modify_gold(-tower_cost)
                self.window.tower_list.append(self.dragged_element)
                self.dragged_element = None

    def gain_gold(self, value):
        self.modify_gold(value)

    def draw(self):
        self.show_gui_elements()
        self.show_dragged_element()
        self.show_tower_popup()
        self.show_info()

    def update(self):
        self.update_dragged_element()
