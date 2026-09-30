"""
GameEngine: owns the frog and all vehicles, and runs one frame's worth
of game logic.

Implemented:
- Correct vehicle collision detection
- 3-life system
- Visible hit feedback
- Respawn
- Game Over
- Goal detection
- Score
- You Won
- 30-second attempt timer
"""

import random
import time

import pygame

from game.frog import Frog
from game.vehicle import Vehicle
from game.collisions import check_collision
from game.renderer import (
    GRID_COLS,
    GRID_ROWS,
    GOAL_ROW,
    ROAD_ROWS,
    START_ROW,
    CELL_SIZE,
    WIDTH,
    HEIGHT,
)


LANE_SPEEDS = [1.5, -2, 2, -2.5, 1.5, -2]

ATTEMPT_TIME = 30


class GameEngine:
    def __init__(self):
        # Lives
        self.lives = 3

        # Score
        self.score = 0

        # Game state
        self.game_over = False
        self.won = False

        # Collision feedback
        self.hit_timer = 0

        # Timer
        self.time_remaining = ATTEMPT_TIME
        self.attempt_start_time = time.monotonic()

        self._build_entities()

    def _build_entities(self):
        start_col = GRID_COLS // 2

        self.frog = Frog(
            col=start_col,
            row=START_ROW,
            start_col=start_col,
            start_row=START_ROW,
            cols=GRID_COLS,
            start_row_limit=START_ROW,
        )

        frog_x_range = (
            start_col * CELL_SIZE,
            start_col * CELL_SIZE + CELL_SIZE,
        )

        self.vehicles = []

        for i, row in enumerate(ROAD_ROWS):
            speed = LANE_SPEEDS[i % len(LANE_SPEEDS)]

            vehicle_width = 40 if i % 2 == 0 else 70
            spacing = 300
            count = 2

            for _attempt in range(20):
                phase = random.randint(0, spacing - 1)
                positions = []
                safe = True

                for n in range(count):
                    offset = phase + n * spacing

                    x = (
                        offset
                        if speed > 0
                        else WIDTH - offset - vehicle_width
                    )

                    positions.append(x)

                    if not (
                        x + vehicle_width <= frog_x_range[0]
                        or x >= frog_x_range[1]
                    ):
                        safe = False

                if safe:
                    break

            for x in positions:
                self.vehicles.append(
                    Vehicle(
                        x=x,
                        row=row,
                        width=vehicle_width,
                        height=CELL_SIZE - 8,
                        speed=speed,
                    )
                )

    def handle_keydown(self, key):

        # R always restarts the whole game
        if key == pygame.K_r:
            self.reset()
            return

        # No movement after win/game over
        if self.game_over or self.won:
            return

        if key == pygame.K_UP:
            self.frog.move(0, -1)

        elif key == pygame.K_DOWN:
            self.frog.move(0, 1)

        elif key == pygame.K_LEFT:
            self.frog.move(-1, 0)

        elif key == pygame.K_RIGHT:
            self.frog.move(1, 0)

    def update(self):

        # Vehicles continue moving
        for v in self.vehicles:
            v.update(road_width_px=WIDTH)

        # Stop everything after game ends
        if self.game_over or self.won:
            return

        # Handle hit feedback
        if self.hit_timer > 0:
            self.hit_timer -= 1

            if self.hit_timer == 0:
                self.frog.reset()
                self._start_new_attempt()

            return

        # Update countdown
        elapsed = time.monotonic() - self.attempt_start_time
        self.time_remaining = max(0, ATTEMPT_TIME - int(elapsed))

        # Timer reached zero
        if self.time_remaining <= 0:
            self._handle_timeout()
            return

        # Check vehicle collision
        if check_collision(self.frog, self.vehicles):
            self._handle_collision()
            return

        # Check goal
        if self.frog.row == GOAL_ROW:
            self._handle_goal()

    def _handle_collision(self):
        """
        Handle collision with a vehicle.
        """

        self.lives -= 1

        if self.lives < 0:
            self.lives = 0

        # Final life lost
        if self.lives == 0:
            self.game_over = True
            self.hit_timer = 0
            return

        # Show hit before respawning
        self.hit_timer = 30

    def _handle_timeout(self):
        """
        A timeout counts as a failed attempt and costs one life.
        """

        self.lives -= 1

        if self.lives < 0:
            self.lives = 0

        # Final life lost
        if self.lives == 0:
            self.game_over = True
            return

        # Give the player another attempt
        self.frog.reset()
        self._start_new_attempt()

    def _start_new_attempt(self):
        """
        Start/restart the 30-second timer for an attempt.
        """

        self.time_remaining = ATTEMPT_TIME
        self.attempt_start_time = time.monotonic()

    def _handle_goal(self):
        """
        Handle successful goal completion.
        """

        self.score += 1
        self.won = True

    def reset(self):
        """
        Completely restart the game.
        """

        self.lives = 3
        self.score = 0

        self.game_over = False
        self.won = False

        self.hit_timer = 0

        self.time_remaining = ATTEMPT_TIME
        self.attempt_start_time = time.monotonic()

        self._build_entities()

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(
            surface,
            self.frog,
            self.vehicles,
        )

        # Lives
        renderer.draw_text(
            surface,
            font,
            f"Lives: {self.lives}",
            (10, 10),
        )

        # Score
        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 34),
        )

        # Timer
        renderer.draw_text(
            surface,
            font,
            f"Time: {self.time_remaining}",
            (10, 58),
        )

        # Controls
        renderer.draw_text(
            surface,
            font,
            "Arrow keys to move. R to restart.",
            (10, HEIGHT - 24),
        )

        # Hit feedback
        if self.hit_timer > 0:
            renderer.draw_banner(
                surface,
                font,
                "HIT!",
            )

        # Game Over
        if self.game_over:
            renderer.draw_banner(
                surface,
                font,
                "GAME OVER - Press R to restart",
            )

        # Win
        if self.won:
            renderer.draw_banner(
                surface,
                font,
                "YOU WON! - Press R to restart",
            )