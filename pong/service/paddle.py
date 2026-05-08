"""Service layer for Paddle movement."""

from pong.types import Paddle, GameState, InputEvent, KeyState
from pong.config import PADDLE_HEIGHT, PADDLE_SPEED, SCREEN_HEIGHT


def update_key_state(key_state: KeyState, event: InputEvent) -> KeyState:
    """Update key state based on input event."""
    key = event.key.lower()
    
    if key == 'w':
        return KeyState(w=event.is_pressed, s=key_state.s, up=key_state.up, down=key_state.down)
    elif key == 's':
        return KeyState(w=key_state.w, s=event.is_pressed, up=key_state.up, down=key_state.down)
    elif key == 'up':
        return KeyState(w=key_state.w, s=key_state.s, up=event.is_pressed, down=key_state.down)
    elif key == 'down':
        return KeyState(w=key_state.w, s=key_state.s, up=key_state.up, down=event.is_pressed)
    
    return key_state


def move_left_paddle(paddle: Paddle, keys: KeyState) -> Paddle:
    """Move left paddle based on key state."""
    if keys.w and not keys.s:
        new_y = max(0, paddle.y - PADDLE_SPEED)
    elif keys.s and not keys.w:
        new_y = min(SCREEN_HEIGHT - paddle.height, paddle.y + PADDLE_SPEED)
    else:
        return paddle
    
    return Paddle(
        x=paddle.x,
        y=new_y,
        height=paddle.height
    )


def move_right_paddle(paddle: Paddle, keys: KeyState) -> Paddle:
    """Move right paddle based on key state."""
    if keys.up and not keys.down:
        new_y = max(0, paddle.y - PADDLE_SPEED)
    elif keys.down and not keys.up:
        new_y = min(SCREEN_HEIGHT - paddle.height, paddle.y + PADDLE_SPEED)
    else:
        return paddle
    
    return Paddle(
        x=paddle.x,
        y=new_y,
        height=paddle.height
    )


def update_paddles(game_state: GameState, keys: KeyState) -> GameState:
    """Update both paddles based on key state."""
    left = move_left_paddle(game_state.left_paddle, keys)
    right = move_right_paddle(game_state.right_paddle, keys)
    
    return GameState(
        ball=game_state.ball,
        left_paddle=left,
        right_paddle=right,
        scores=game_state.scores,
        game_over=game_state.game_over,
        winner=game_state.winner
    )
