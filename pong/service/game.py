"""Service layer for Pong game - main game loop and state management."""

from pong.types import GameState, Ball, Paddle, Scores, InputEvent, KeyState
from pong.config import WIN_SCORE, SCREEN_WIDTH
from pong.service.ball import (
    update_ball,
    handle_wall_collision,
    handle_paddle_collision,
    check_score,
    reset_ball,
    move_paddle,
    create_initial_state,
)
from pong.service.paddle import update_paddles


def update_game_state(
    game_state: GameState,
    keys: KeyState
) -> GameState:
    """Update the complete game state for one frame."""
    if game_state.game_over:
        return game_state
    
    # Update paddles
    state = update_paddles(game_state, keys)
    
    # Update ball
    ball = update_ball(state.ball)
    
    # Handle wall collisions
    ball = handle_wall_collision(ball)
    
    # Handle paddle collisions
    ball = handle_paddle_collision(ball, state.left_paddle, state.right_paddle)
    
    # Check for score
    scored, scorer = check_score(ball, state.left_paddle, state.right_paddle)
    
    if scored:
        if scorer == 'left':
            new_scores = Scores(
                left=state.scores.left + 1,
                right=state.scores.right
            )
        else:
            new_scores = Scores(
                left=state.scores.left,
                right=state.scores.right + 1
            )
        
        # Check win condition
        if new_scores.left >= WIN_SCORE or new_scores.right >= WIN_SCORE:
            winner = 'left' if new_scores.left >= WIN_SCORE else 'right'
            return GameState(
                ball=reset_ball(),
                left_paddle=state.left_paddle,
                right_paddle=state.right_paddle,
                scores=new_scores,
                game_over=True,
                winner=winner
            )
        
        # Reset ball after score
        return GameState(
            ball=reset_ball(),
            left_paddle=state.left_paddle,
            right_paddle=state.right_paddle,
            scores=new_scores,
            game_over=False,
            winner=None
        )
    
    return GameState(
        ball=ball,
        left_paddle=state.left_paddle,
        right_paddle=state.right_paddle,
        scores=state.scores,
        game_over=False,
        winner=None
    )


def create_new_game() -> GameState:
    """Create a fresh game state."""
    state = create_initial_state()
    return GameState(
        ball=state.ball,
        left_paddle=state.left_paddle,
        right_paddle=state.right_paddle,
        scores=Scores(left=0, right=0),
        game_over=False,
        winner=None
    )
