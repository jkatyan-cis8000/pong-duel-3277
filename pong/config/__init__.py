"""Config module for Pong game."""

from .settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PADDLE_HEIGHT,
    PADDLE_WIDTH,
    PADDLE_OFFSET,
    PADDLE_SPEED,
    BALL_RADIUS,
    BALL_SPEED,
    INITIAL_BALL_SPEED,
    WIN_SCORE,
    COLOR_FG,
    COLOR_BG,
)

from .keys import (
    LEFT_UP,
    LEFT_DOWN,
    RIGHT_UP,
    RIGHT_DOWN,
    ALL_KEYS,
)

__all__ = [
    # Screen
    'SCREEN_WIDTH',
    'SCREEN_HEIGHT',
    # Paddle
    'PADDLE_HEIGHT',
    'PADDLE_WIDTH',
    'PADDLE_OFFSET',
    'PADDLE_SPEED',
    # Ball
    'BALL_RADIUS',
    'BALL_SPEED',
    'INITIAL_BALL_SPEED',
    # Game
    'WIN_SCORE',
    # Colors
    'COLOR_FG',
    'COLOR_BG',
    # Keys
    'LEFT_UP',
    'LEFT_DOWN',
    'RIGHT_UP',
    'RIGHT_DOWN',
    'ALL_KEYS',
]
