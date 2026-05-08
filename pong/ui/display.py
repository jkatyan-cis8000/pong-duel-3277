"""UI layer for displaying messages."""

from pong.types import GameState


def show_title() -> None:
    """Show game title screen."""
    print("=" * 80)
    print(" " * 30 + "PONG DUEL")
    print(" " * 20 + "Left: W/S  |  Right: Up/Down")
    print(" " * 25 + "First to 5 wins!")
    print("=" * 80)
    print()


def show_instructions() -> None:
    """Show controls."""
    print("CONTROLS:")
    print("  Left Player:  'W' = Up, 'S' = Down")
    print("  Right Player: 'Up Arrow' = Up, 'Down Arrow' = Down")
    print("  Quit:         'Q' or Ctrl+C")
    print()


def show_game_over(winner: str) -> None:
    """Show game over message."""
    print()
    print("=" * 40)
    print(f"  GAME OVER - {winner.upper()} WINS!")
    print("=" * 40)
    print()
