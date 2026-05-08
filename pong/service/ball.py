"""Service layer for Pong game - ball movement and collision."""

from pong.types import Ball, Position, Velocity, Paddle, GameState, InputEvent
from pong.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BALL_RADIUS,
    PADDLE_HEIGHT,
    PADDLE_OFFSET,
    PADDLE_WIDTH,
)


def reset_ball() -> Ball:
    """Create a new ball at center with random direction."""
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2
    
    # Random direction (left or right, slight random angle)
    import random
    dx = random.choice([-1, 1]) * 1
    dy = random.choice([-1, 1]) * 1
    
    return Ball(
        position=Position(x=center_x, y=center_y),
        velocity=Velocity(dx=dx, dy=dy)
    )


def create_initial_paddles() -> tuple[Paddle, Paddle]:
    """Create paddles at starting positions."""
    left_y = (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2
    right_y = (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2
    
    left = Paddle(
        x=PADDLE_OFFSET,
        y=left_y,
        height=PADDLE_HEIGHT
    )
    
    right = Paddle(
        x=SCREEN_WIDTH - PADDLE_OFFSET - PADDLE_WIDTH,
        y=right_y,
        height=PADDLE_HEIGHT
    )
    
    return left, right


def create_initial_state() -> GameState:
    """Create the initial game state."""
    ball = reset_ball()
    left_paddle, right_paddle = create_initial_paddles()
    
    return GameState(
        ball=ball,
        left_paddle=left_paddle,
        right_paddle=right_paddle,
        scores=None,  # Will be set separately
        game_over=False,
        winner=None
    )


def create_initial_scores() -> GameState:
    """Create state with zero scores."""
    state = create_initial_state()
    return GameState(
        ball=state.ball,
        left_paddle=state.left_paddle,
        right_paddle=state.right_paddle,
        scores=state.scores if state.scores else None,
        game_over=False,
        winner=None
    )


def move_paddle(paddle: Paddle, direction: str, max_y: int) -> Paddle:
    """Move paddle up or down."""
    if direction == 'up':
        new_y = max(0, paddle.y - 1)
    elif direction == 'down':
        new_y = min(max_y - paddle.height, paddle.y + 1)
    else:
        return paddle
    
    return Paddle(
        x=paddle.x,
        y=new_y,
        height=paddle.height
    )


def check_collision(ball: Ball, paddle: Paddle) -> bool:
    """Check if ball collides with paddle."""
    # Check horizontal overlap
    ball_left = ball.position.x
    ball_right = ball.position.x
    paddle_left = paddle.x
    paddle_right = paddle.x + PADDLE_WIDTH
    
    horizontal_overlap = not (ball_right < paddle_left or ball_left > paddle_right)
    
    # Check vertical overlap
    ball_top = ball.position.y
    ball_bottom = ball.position.y
    paddle_top = paddle.y
    paddle_bottom = paddle.y + paddle.height
    
    vertical_overlap = not (ball_bottom < paddle_top or ball_top > paddle_bottom)
    
    return horizontal_overlap and vertical_overlap


def update_ball(ball: Ball) -> Ball:
    """Update ball position based on velocity."""
    new_x = ball.position.x + ball.velocity.dx
    new_y = ball.position.y + ball.velocity.dy
    
    return Ball(
        position=Position(x=new_x, y=new_y),
        velocity=ball.velocity
    )


def handle_wall_collision(ball: Ball) -> Ball:
    """Handle ball collision with top and bottom walls."""
    if ball.position.y <= 0 or ball.position.y >= SCREEN_HEIGHT - 1:
        new_velocity = Velocity(
            dx=ball.velocity.dx,
            dy=-ball.velocity.dy
        )
        return Ball(
            position=ball.position,
            velocity=new_velocity
        )
    return ball


def handle_paddle_collision(ball: Ball, left_paddle: Paddle, right_paddle: Paddle) -> Ball:
    """Handle ball collision with paddles."""
    # Check left paddle
    if check_collision(ball, left_paddle) and ball.velocity.dx < 0:
        new_velocity = Velocity(
            dx=-ball.velocity.dx,  # Reverse horizontal direction
            dy=ball.velocity.dy
        )
        # Move ball slightly away from paddle to prevent sticking
        new_x = left_paddle.x + PADDLE_WIDTH + 1
        return Ball(
            position=Position(x=new_x, y=ball.position.y),
            velocity=new_velocity
        )
    
    # Check right paddle
    if check_collision(ball, right_paddle) and ball.velocity.dx > 0:
        new_velocity = Velocity(
            dx=-ball.velocity.dx,  # Reverse horizontal direction
            dy=ball.velocity.dy
        )
        # Move ball slightly away from paddle to prevent sticking
        new_x = right_paddle.x - 1
        return Ball(
            position=Position(x=new_x, y=ball.position.y),
            velocity=new_velocity
        )
    
    return ball


def check_score(ball: Ball, left_paddle: Paddle, right_paddle: Paddle) -> tuple[bool, str]:
    """Check if a player scored. Returns (scored, scorer)."""
    if ball.position.x < 0:
        return True, 'right'
    if ball.position.x >= SCREEN_WIDTH:
        return True, 'left'
    return False, ''
