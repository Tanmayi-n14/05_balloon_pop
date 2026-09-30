"""
GameEngine: owns all balloons, spawns new ones, updates game state,
tracks score, lives, and countdown timer.
"""

import random
import pygame

from game.balloon import Balloon
from game.click_detection import check_pop
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 45
GAME_DURATION_SECONDS = 30
STARTING_LIVES = 3


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.balloons = []
        self.frames_until_spawn = 0
        self.score = 0
        self.lives = STARTING_LIVES
        self.time_remaining = float(GAME_DURATION_SECONDS)
        self.is_game_over = False

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
        if self.is_game_over:
            return

        popped = check_pop(self.balloons, pos)
        if popped is not None:
            self.balloons.remove(popped)
            self.score = max(0, self.score + popped.points)

    def handle_key(self, key):
        if self.is_game_over and key == pygame.K_r:
            self.reset()

    def update(self, dt):
        if self.is_game_over:
            return

        # Decrement timer
        self.time_remaining -= dt
        if self.time_remaining <= 0:
            self.time_remaining = 0
            self.is_game_over = True
            return

        # Spawning
        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_balloon()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        # Update balloons & handle missed ones
        surviving_balloons = []
        for b in self.balloons:
            b.update()
            if b.is_past_bottom(HEIGHT):
                # Missed balloon costs a life
                self.lives -= 1
                if self.lives <= 0:
                    self.lives = 0
                    self.is_game_over = True
            else:
                surviving_balloons.append(b)

        self.balloons = surviving_balloons

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(surface, self.balloons)

        # HUD
        renderer.draw_text(surface, font, f"Score: {self.score}", (15, 12))
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (200, 12))
        renderer.draw_text(
            surface, font, f"Time: {int(self.time_remaining)}s", (WIDTH - 130, 12)
        )

        if self.is_game_over:
            renderer.draw_banner(
                surface, font, f"GAME OVER! Final Score: {self.score}"
            )
            renderer.draw_text(
                surface,
                font,
                "Press 'R' to Restart",
                (WIDTH // 2 - 100, HEIGHT // 2 + 40),
            )