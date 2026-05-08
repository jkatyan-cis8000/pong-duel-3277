"""Provider layer for display/output."""

from pong.types import GameState, Scores


class DisplayProvider:
    """Provides terminal display rendering."""
    
    def clear(self) -> None:
        """Clear the terminal screen."""
        print('\033[2J\033[H', end='')
    
    def render_game(self, game_state: GameState) -> None:
        """Render the current game state."""
        # Build screen buffer
        height = 24
        width = 80
        buffer = [[' ' for _ in range(width)] for _ in range(height)]
        
        # Draw paddles
        self._draw_paddle(buffer, game_state.left_paddle, 'O')
        self._draw_paddle(buffer, game_state.right_paddle, 'X')
        
        # Draw ball
        ball = game_state.ball
        if 0 <= ball.position.y < height and 0 <= ball.position.x < width:
            buffer[ball.position.y][ball.position.x] = '@'
        
        # Draw border
        for x in range(width):
            buffer[0][x] = '-'
            buffer[height - 1][x] = '-'
        for y in range(height):
            buffer[y][0] = '|'
            buffer[y][width - 1] = '|'
        
        # Print score
        score = game_state.scores
        score_text = f"Left: {score.left} | Right: {score.right}"
        if len(score_text) < width - 2:
            buffer[0][2:2 + len(score_text)] = list(score_text)
        
        # Print game over message
        if game_state.game_over:
            msg = f"GAME OVER - {game_state.winner.upper()} WINS!"
            msg_y = height // 2
            start_x = (width - len(msg)) // 2
            buffer[msg_y][start_x:start_x + len(msg)] = list(msg)
        
        # Render buffer
        for row in buffer:
            print(''.join(row))
    
    def _draw_paddle(self, buffer: list[list[str]], paddle, char: str) -> None:
        """Draw a paddle on the buffer."""
        for y in range(paddle.y, paddle.y + paddle.height):
            if 0 <= y < len(buffer):
                for x in range(paddle.x, paddle.x + 3):
                    if 0 <= x < len(buffer[0]):
                        buffer[y][x] = char
