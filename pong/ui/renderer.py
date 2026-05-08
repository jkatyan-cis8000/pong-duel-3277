"""UI layer for Pong game - rendering."""

from pong.types import GameState
from pong.providers import DisplayProvider


class GameRenderer:
    """Renders the game state to the terminal."""
    
    def __init__(self):
        self.display = DisplayProvider()
    
    def render(self, game_state: GameState) -> None:
        """Render the game state."""
        self.display.render_game(game_state)
