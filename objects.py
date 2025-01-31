import arcade
import math
import copy
import enum
from arcade import SpriteList
from const import ENEMIES, TOWERS, HP_BAR


class MiniTower(arcade.Sprite):
    def __init__(self, x, y, _type=1):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.scale = 0.5
        self.tower_type = _type
        self.cost = None
        self.disabled = True
        self.show_popup = False
        self.texture_path = f"media/t{self.tower_type}.png"

        self._setup_tower()
        self._load_textures()

    def _setup_tower(self):
        self.cost = TOWERS[f"type_{self.tower_type}"]["cost"]

    def _load_textures(self):
        texture = arcade.load_texture(self.texture_path, x=0, y=0, width=48, height=54)
        self.texture = texture

    def show_info_popup(self):
        if self.show_popup:
            arcade.draw_text(f"Cost: {self.cost}",
                             self.center_x,
                             self.center_y,
                             arcade.color.BLACK,
                             15,
                             font_name="GodOfWar")

    def draw(self):
        self.show_info_popup()
        super().draw()


class Bullet(arcade.Sprite):
    def __init__(self, start_x, start_y, target, damage, speed, bullet_texture, predicted_location_x, predicted_location_y):
        super().__init__()
        self.center_x = start_x
        self.center_y = start_y
        self.scale = 0.2
        self.damage = damage
        self.speed = speed
        self.change_x = 0
        self.change_y = 0
        self.angle = 0
        self.target = target

        self._load_textures(bullet_texture)
        self.set_target(predicted_location_x, predicted_location_y)

    def _load_textures(self, texture):
        self.texture = arcade.load_texture(texture, hit_box_detail=2, hit_box_algorithm="Detailed")

    def set_target(self, predicted_location_x, predicted_location_y):
        self.angle = math.atan2(predicted_location_y - self.center_y, predicted_location_x - self.center_x)
        self.change_x = math.cos(self.angle) * self.speed
        self.change_y = math.sin(self.angle) * self.speed

    def rotate_bullet(self):
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x)) - 90

    def check_if_out_of_map(self):
        if self.center_x < 0 or self.center_x > 1024 or self.center_y < 0 or self.center_y > 786:
            self.kill()

    def check_if_target_reached(self, targets):
        # Bullet can be shot very fast so we need to verify
        # if the enemy is on the line
        target_hit_list = arcade.get_sprites_at_point((self.center_x, self.center_y), targets)
        for _target in target_hit_list:
            _target.current_health -= self.damage
            self.kill()
        self.check_if_out_of_map()

    def draw(self):
        super().draw()
        self.draw_hit_box()

    def update(self, enemy_list):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.rotate_bullet()
        self.check_if_target_reached(enemy_list)


class Tower(arcade.Sprite):
    def __init__(self, x, y, _type=1):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.scale = 1
        self.tower_type = _type
        self.angle = 90
        self.state = 'idle'
        self.aimed_enemy = None
        self.enemy_list = None
        self.animation_textures = None
        self.tower_selected = False
        self.bullet_texture = "media/bullet.png"
        self.bullets_fired = SpriteList()
        self.attack_counter = 9999

        self._initial_settings()
        self._load_textures()

    def _initial_settings(self):
        config = TOWERS[f"type_{self.tower_type}"]
        self.damage = config.get("damage", 10)
        self.range = config.get("range", 100)
        self.attack_speed = config.get("attack_speed", 1)
        self.cost = config.get("cost", 50)
        self.bullet_speed = config.get("bullet_speed", 5)

        # Create a deep copy of the animation textures, so we can modify it without changing the original
        self.animation_textures = copy.deepcopy(config["animation_textures"])

    def _load_textures(self):
        texture = arcade.load_texture(f"media/t{self.tower_type}.png", x=0, y=0, width=48, height=54)
        self.animation_textures['idle']['textures'].append(texture)

        self.texture = self.animation_textures['idle']['textures'][0]

    def calculate_intercept_point(self):
        dx = self.aimed_enemy.center_x - self.center_x
        dy = self.aimed_enemy.center_y - self.center_y

        v2 = self.aimed_enemy.change_x ** 2 + self.aimed_enemy.change_y ** 2 - self.bullet_speed ** 2

        a = v2
        b = 2 * (dx * self.aimed_enemy.change_x + dy * self.aimed_enemy.change_y)
        c = dx ** 2 + dy ** 2

        delta = b ** 2 - 4 * a * c

        if delta < 0:
            return None

        t1 = (-b + math.sqrt(delta)) / (2 * a)
        t2 = (-b - math.sqrt(delta)) / (2 * a)
        t = max(t1, t2)

        if t < 0:
            return None
        intercept_x = self.aimed_enemy.center_x + self.aimed_enemy.change_x * t
        intercept_y = self.aimed_enemy.center_y + self.aimed_enemy.change_y * t

        return intercept_x, intercept_y

    def rotate_where_target(self):
        if self.aimed_enemy is None:
            return
        self.angle = -arcade.get_angle_degrees(self.center_x, self.center_y,
                                               self.aimed_enemy.center_x, self.aimed_enemy.center_y)

    def draw(self):
        super().draw()
        self.draw_bullets()

    def show_range(self):
        # Draw at the top of all elements
        arcade.draw_circle_outline(self.center_x, self.center_y, self.range, arcade.color.WHITE_SMOKE, 2)
        # Transparent circle
        arcade.draw_circle_filled(self.center_x, self.center_y, self.range, arcade.color.WHITE_SMOKE + (50,))

    def show_aimed_enemy(self):
        if self.aimed_enemy is not None:
            arcade.draw_line(self.center_x, self.center_y, self.aimed_enemy.center_x, self.aimed_enemy.center_y,
                             arcade.color.RED, 2)

    def look_for_enemy(self):
        if self.aimed_enemy is None:
            return True
        if self.aimed_enemy not in self.enemy_list:
            self.reset_aimed_enemy()
            return True

        distance_to_enemy = arcade.get_distance(self.center_x, self.center_y,
                                                self.aimed_enemy.center_x, self.aimed_enemy.center_y)
        if distance_to_enemy > self.range:
            self.reset_aimed_enemy()
            return True

        return False

    def reset_aimed_enemy(self):
        self.aimed_enemy = None

    def get_closest_enemy(self):
        if not self.enemy_list:
            return
        enemy, distance = arcade.get_closest_sprite(self, self.enemy_list)
        if distance < self.range:
            self.aimed_enemy = enemy

    def aim_enemy(self, enemy_list):
        self.update_enemy_list(enemy_list)
        if self.look_for_enemy():
            self.get_closest_enemy()

    def shoot(self):
        predicted_location_x, predicted_location_y = self.calculate_intercept_point()
        if predicted_location_x is None or predicted_location_y is None:
            predicted_location_x = self.aimed_enemy.center_x
            predicted_location_y = self.aimed_enemy.center_y
        bullet = Bullet(self.center_x, self.center_y,
                        self.aimed_enemy, self.damage,
                        self.bullet_speed, self.bullet_texture,
                        predicted_location_x, predicted_location_y)
        self.bullets_fired.append(bullet)

    def attack(self, delta_time: float = 1/60):
        # Attack with the speed of the tower, if attack speed is 1,
        # then it is 1 attack per second, if 0.5, then 2 attacks per second
        if self.aimed_enemy is not None:
            self.attack_counter += delta_time
            if self.attack_counter > self.attack_speed:
                self.attack_counter = 0
                self.shoot()

    def update_enemy_list(self, enemy_list):
        self.enemy_list = enemy_list

    def update_bullets(self):
        for bullet in self.bullets_fired:
            bullet.update(self.enemy_list)

    def draw_bullets(self):
        for bullet in self.bullets_fired:
            bullet.draw()

    def update(self, delta_time: float = 1/60):
        super().update()
        self.rotate_where_target()
        self.attack(delta_time)
        self.update_bullets()


class Enemy(arcade.Sprite):
    def __init__(self, x, y, point_list, _type=1):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.scale = 0.4
        self.enemy_type = _type
        self.angle = 90
        self.state = 'idle'
        self.movement_speed = None
        self.animation_textures = None
        self.next_point = None
        self.move_points = point_list
        self.texture_path = None

        self._initialize_properties()
        self._load_textures_custom()

    def _initialize_properties(self):
        config = ENEMIES[f"type_{self.enemy_type}"]
        self.health = config.get("health", 100)
        self.current_health = self.health
        self.reward = config.get("reward", 10)
        self.damage = config.get("damage", 10)
        self.movement_speed = config.get("speed", None)
        self.hp_bar = HP_BAR
        self.next_point = self.move_points.pop(0)
        self.texture_path = f"media/e{self.enemy_type}.png"

        # Create a deep copy of the animation textures, so we can modify it without changing the original
        self.animation_textures = copy.deepcopy(config["animation_textures"])

    def _load_textures_custom(self):
        for i in range(9):
            texture = arcade.load_texture(self.texture_path, x=i * 64, y=0, width=64, height=64)
            self.animation_textures['moving']['textures'].append(texture)

        self.texture = self.animation_textures['moving']['textures'][0]

    def _change_state(self, state):
        self.previous_state = self.state
        self.state = state

    def change_state(self, state):
        self._change_state(state)
        self._reset_texture_collection()

    def _reset_texture_collection(self):
        self.textures = self.animation_textures[self.state]["textures"]
        self.animation_textures[self.state]["frame_count"] = 0
        self.set_texture(0)

    def is_point_reached(self):
        # Sprites move is counted in pixels, but it is float, so we need to check if it is close to the point
        if abs(self.center_x - self.next_point[0]) < 2 and abs(self.center_y - self.next_point[1]) < 2:
            return True
        return False

    def rotate_sprite(self):
        self.angle = -arcade.get_angle_degrees(self.center_x, self.center_y, self.next_point[0], self.next_point[1])

    def calculate_speed(self):
        c_x = (math.cos(
            math.atan2(self.next_point[1] - self.center_y, self.next_point[0] - self.center_x))
               * self.movement_speed["movement_treshhold"]
               )
        c_y = (math.sin(
            math.atan2(self.next_point[1] - self.center_y, self.next_point[0] - self.center_x))
               * self.movement_speed["movement_treshhold"]
               )
        return c_x, c_y

    def move(self):
        if self.is_point_reached():
            if len(self.move_points) > 0:
                self.next_point = self.move_points.pop(0)
            self.rotate_sprite()
            # Set speed and direction
        self.change_x, self.change_y = self.calculate_speed()
        #self.if_out_of_map()

    def execute_state(self):
        if self.state == "moving":
            self.move()

    # def if_out_of_map(self):
    #     if self.center_x < 0 or self.center_x > 1024 or self.center_y < 0 or self.center_y > 786:
    #         print("YOU LOSE")

    def draw_health_bar(self):
        if self.current_health > 0:
            current_bar_width = (self.current_health / self.health) * self.hp_bar["width"]
            left_bar_x = self.center_x - (self.hp_bar["width"] / 2)

            arcade.draw_rectangle_filled(self.center_x, self.center_y + self.hp_bar["y_shift"],
                                         self.hp_bar["width"], self.hp_bar["height"], self.hp_bar["color_low"])
            arcade.draw_rectangle_filled(left_bar_x + (current_bar_width / 2), self.center_y + self.hp_bar["y_shift"],
                                         current_bar_width, self.hp_bar["height"],
                                         self.hp_bar["color_high"])

    def animation_update(self):
        state = self.animation_textures[self.state]
        state["frame_count"] += 1
        if state["frame_count"] % state["update_rate"] == 0:
            current_texture_index = (state["frame_count"] // state["update_rate"]) % len(self.textures)
            self.set_texture(current_texture_index)
        # If the animation has reached the end, reset it to avoid overflow
        if state["frame_count"] % (len(self.textures) * state["update_rate"]) == 0:
            state["frame_count"] = 0

    def draw(self):
        super().draw()
        self.draw_hit_box()
        self.draw_health_bar()

    def update(self):
        super().update()
        self.execute_state()
        self.animation_update()


class Enemy1(Enemy):
    def __init__(self, x, y, point_list):
        super().__init__(x, y, point_list, 1)


class Enemy2(Enemy):
    def __init__(self, x, y, point_list):
        super().__init__(x, y, point_list, 2)


class Enemy3(Enemy):
    def __init__(self, x, y, point_list):
        super().__init__(x, y, point_list, 3)


class EnemyEnum(enum.Enum):
    TYPE_1 = Enemy1
    TYPE_2 = Enemy2
    TYPE_3 = Enemy3
