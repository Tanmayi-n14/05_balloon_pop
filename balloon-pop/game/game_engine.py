"""
GameEngine: owns all balloons, spawns new ones, and handles clicks.
"""

import random

from game.balloon import Balloon
from game.click_detection import check_pop
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 45
STARTING_LIVES = 3


class GameEngine:
    def __init__(self):
        self.balloons = []
        self.frames_until_spawn = 0
        self.score = 0
        self.lives = STARTING_LIVES

    def _spawn_balloon(self):
        radius = random.randint(18, 42)
        x = random.randint(radius + 10, WIDTH - radius - 10)
        speed = random.uniform(1.8, 3.2)

        b_type = random.choices(
            [Balloon.TYPE_NORMAL, Balloon.TYPE_BONUS, Balloon.TYPE_PENALTY],
            weights=[65, 20, 15],
            k=1,
        )[0]

        self.balloons.append(
            Balloon(x=x, y=-radius, radius=radius, speed=speed, balloon_type=b_type)
        )

    def handle_click(self, pos):
        if self.lives <= 0:
            return

        popped = check_pop(self.balloons, pos)
        if popped is not None:
            self.balloons.remove(popped)
            self.score = max(0, self.score + popped.points)

    def update(self):
        if self.lives <= 0:
            return

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_balloon()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        surviving_balloons = []
        for b in self.balloons:
            b.update()
            if b.is_past_bottom(HEIGHT):
                self.lives -= 1
            else:
                surviving_balloons.append(b)

        self.balloons = surviving_balloons

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.balloons)
        renderer.draw_text(surface, font, f"Score: {self.score}", (15, 12))
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (200, 12))