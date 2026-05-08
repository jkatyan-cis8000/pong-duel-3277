"""Runtime layer for Pong game - event loop."""

import time
import sys
from pong.types import InputEvent, KeyState, GameState
from pong.config import WIN_SCORE, SCREEN_WIDTH, SCREEN_HEIGHT
from pong.service import update_game_state, create_new_game
from pong.providers import InputProvider, DisplayProvider
from pong.repo import load_high_score, update_high_score


class GameLoop:
    """Main game loop orchestrator."""
    
    def __init__(self):
        self.input_provider = InputProvider()
        self.display = DisplayProvider()
        self.keys = KeyState()
        self.game_state: GameState | None = None
    
    def _show_title(self) -> None:
        """Show game title screen."""
        print("=" * SCREEN_WIDTH)
        print(" " * (SCREEN_WIDTH // 2 - 5) + "PONG DUEL")
        print(" " * (SCREEN_WIDTH // 4) + "Left: W/S  |  Right: Up/Down")
        print(" " * (SCREEN_WIDTH // 2 - 7) + "First to 5 wins!")
        print("=" * SCREEN_WIDTH)
        print()
    
    def _show_instructions(self) -> None:
        """Show controls."""
        print("CONTROLS:")
        print("  Left Player:  'W' = Up, 'S' = Down")
        print("  Right Player: 'Up Arrow' = Up, 'Down Arrow' = Down")
        print("  Quit:         'Q' or Ctrl+C")
        print()
    
    def _show_game_over(self, winner: str) -> None:
        """Show game over message."""
        print()
        print("=" * 40)
        print(f"  GAME OVER - {winner.upper()} WINS!")
        print("=" * 40)
        print()
    
    def run(self) -> None:
        """Run the main game loop."""
        self._show_title()
        self._show_instructions()
        
        try:
            self.game_state = create_new_game()
            high_score = load_high_score()
            
            with self.input_provider:
                while True:
                    # Poll input
                    events = self.input_provider.poll()
                    for event in events:
                        self._handle_input(event)
                    
                    # Update game state
                    if self.game_state and not self.game_state.game_over:
                        self.game_state = update_game_state(self.game_state, self.keys)
                        
                        # Render
                        self.display.clear()
                        self._render_game_state()
                        
                        # Wait for next frame
                        time.sleep(0.1)
                    elif self.game_state and self.game_state.game_over:
                        self.display.clear()
                        self._render_game_state()
                        
                        # Show game over
                        self._show_game_over(self.game_state.winner)
                        
                        # Check high score
                        update_high_score(high_score, self.game_state.scores)
                        
                        print(f"\nFinal Score: Left {self.game_state.scores.left} - Right {self.game_state.scores.right}")
                        print("Press Enter to play again or 'Q' to quit...")
                        
                        # Wait for restart or quit
                        while True:
                            events = self.input_provider.poll()
                            for event in events:
                                if event.key == 'enter':
                                    self.game_state = create_new_game()
                                    high_score = load_high_score()
                                    break
                                elif event.key.lower() == 'q':
                                    return
                            time.sleep(0.1)
                        continue
                    
        except KeyboardInterrupt:
            print("\nGame interrupted.")
    
    def _render_game_state(self) -> None:
        """Render the current game state to terminal."""
        if self.game_state is None:
            return
        
        # Build screen buffer
        height = SCREEN_HEIGHT
        width = SCREEN_WIDTH
        buffer = [[' ' for _ in range(width)] for _ in range(height)]
        
        # Draw paddles
        self._draw_paddle(buffer, self.game_state.left_paddle, 'O')
        self._draw_paddle(buffer, self.game_state.right_paddle, 'X')
        
        # Draw ball
        ball = self.game_state.ball
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
        score = self.game_state.scores
        score_text = f"Left: {score.left} | Right: {score.right}"
        if len(score_text) < width - 2:
            buffer[0][2:2 + len(score_text)] = list(score_text)
        
        # Print game over message
        if self.game_state.game_over:
            msg = f"GAME OVER - {self.game_state.winner.upper()} WINS!"
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
    
    def _handle_input(self, event: InputEvent) -> None:
        """Handle input event."""
        if event.key.lower() == 'q':
            raise KeyboardInterrupt()
        
        # Update key state for paddle movement
        from pong.service.paddle import update_key_state
        self.keys = update_key_state(self.keys, event)
