ENEMIES = {
    "type_1": {
        "health": 20,
        "reward": 15,
        "damage": 10,
        "speed": {
            "movement_treshhold": 0.6,
            "movement_counter": 0,
            "movement_speed": 10
        },
        "animation_textures": {
            'idle': {
                'frame_rate': 0,
                'update_rate': 1,
                'textures': []
            },
            'moving': {
                'frame_rate': 0,
                'update_rate': 10,
                'textures': []
            },
        }
    },
    "type_2": {
        "health": 40,
        "reward": 25,
        "damage": 15,
        "speed": {
            "movement_treshhold": 1,
            "movement_counter": 0,
            "movement_speed": 15
        },
        "animation_textures": {
            'idle': {
                'frame_rate': 0,
                'update_rate': 1,
                'textures': []
            },
            'moving': {
                'frame_rate': 0,
                'update_rate': 10,
                'textures': []
            },
        }
    },
    "type_3": {
        "health": 120,
        "reward": 50,
        "damage": 20,
        "speed": {
            "movement_treshhold": 1.2,
            "movement_counter": 0,
            "movement_speed": 30
        },
        "animation_textures": {
            'idle': {
                'frame_rate': 0,
                'update_rate': 1,
                'textures': []
            },
            'moving': {
                'frame_rate': 0,
                'update_rate': 10,
                'textures': []
            },
        }
    }
}

TOWERS = {
    "type_1": {
        "range": 120,
        "damage": 5,
        "attack_speed": 0.9,
        "animation_textures": {
            'idle': {
                'frame_rate': 0,
                'update_rate': 1,
                'textures': []
            },
            'attack': {
                'frame_rate': 0,
                'update_rate': 10,
                'textures': []
            },
        },
        "cost": 50,
        "bullet_speed": 2,
    },
    "type_2": {
        "range": 240,
        "damage": 2,
        "attack_speed": 0.2,
        "animation_textures": {
            'idle': {
                'frame_rate': 0,
                'update_rate': 1,
                'textures': []
            },
            'attack': {
                'frame_rate': 0,
                'update_rate': 10,
                'textures': []
            },
        },
        "cost": 100,
        "bullet_speed": 7,
    },
    "type_3": {
        "range": 200,
        "damage": 15,
        "attack_speed": 2,
        "animation_textures": {
            'idle': {
                'frames_counter': 0,
                'update_rate': 1,
                'textures': []
            },
            'attack': {
                'frames_counter': 0,
                'update_rate': 10,
                'textures': []
            },
        },
        "cost": 150,
        "bullet_speed": 2,
    },
    "type_4": {
        "range": 250,
        "damage": 10,
        "attack_speed": 0.5,
        "animation_textures": {
            'idle': {
                'frames_counter': 0,
                'update_rate': 1,
                'textures': []
            },
            'attack': {
                'frames_counter': 0,
                'update_rate': 10,
                'textures': []
            },
        },
        "cost": 300,
        "bullet_speed": 10,
    }
}

MAP_POINTS = {
    "MAP_1": {
        "points": [
            [945, 620],  # 0
            [945, 145],  # 1
            [735, 145],  # 2
            [735, 630],  # 3
            [560, 620],  # 4
            [550, 440],  # 5
            [665, 440],  # 6
            [665, 150],  # 7
            [395, 150],  # 8
            [390, 275],  # 9
            [485, 280],  # 10
            [485, 360],  # 11
            [-100, 360],   # 12
        ],
        "enemies": {
                "TYPE_1": 10,  # how many
                "TYPE_2": 5,
                "TYPE_3": 1,
            },
        "enemies_start_point": [1015, 620],
        "enemy_spawn": 1  # 1 second
    }
}

HP_BAR = {
    "width": 20,
    "height": 5,
    "color_low": (255, 0, 0),
    "color_high": (0, 255, 0),
    "y_shift": 20
}


