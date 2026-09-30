"""
Balloon: falls from the top of the screen. The player must pop it
before it reaches the bottom. Balloons vary in size, points, and type.
"""

import pygame


class Balloon:
    TYPE_NORMAL = "normal"
    TYPE_BONUS = "bonus"
    TYPE_PENALTY = "penalty"

    CONFIGS = {
        TYPE_NORMAL: {"color": (230, 70, 90), "points": 10},
        TYPE_BONUS: {"color": (245, 195, 35), "points": 25},
        TYPE_PENALTY: {"color": (60, 60, 70), "points": -15},
    }

    def __init__(self, x, y, radius, speed, balloon_type=TYPE_NORMAL):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.balloon_type = balloon_type

        config = self.CONFIGS[balloon_type]
        self.color = config["color"]
        self.points = config["points"]

    def update(self):
        self.y += self.speed

    def is_past_bottom(self, height):
        return self.y - self.radius > height

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )