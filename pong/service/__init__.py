"""Service module for Pong game."""

from .ball import (
    reset_ball,
    create_initial_paddles,
    create_initial_state,
    create_initial_scores,
    move_paddle,
    check_collision,
    update_ball,
    handle_wall_collision,
    handle_paddle_collision,
    check_score,
)

from .paddle import (
    update_key_state,
    move_left_paddle,
    move_right_paddle,
    update_paddles,
)

from .game import (
    update_game_state,
    create_new_game,
)

__all__ = [
    # Ball
    'reset_ball',
    'create_initial_paddles',
    'create_initial_state',
    'create_initial_scores',
    'move_paddle',
    'check_collision',
    'update_ball',
    'handle_wall_collision',
    'handle_paddle_collision',
    'check_score',
    # Paddle
    'update_key_state',
    'move_left_paddle',
    'move_right_paddle',
    'update_paddles',
    # Game
    'update_game_state',
    'create_new_game',
]
