"""Types for the Pong game."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    """Represents a position on the game board."""
    x: int
    y: int


@dataclass(frozen=True)
class Velocity:
    """Represents velocity (speed and direction)."""
    dx: int
    dy: int


@dataclass(frozen=True)
class Ball:
    """Represents the game ball."""
    position: Position
    velocity: Velocity


@dataclass(frozen=True)
class Paddle:
    """Represents a player's paddle."""
    x: int
    y: int
    height: int


@dataclass(frozen=True)
class Scores:
    """Player scores."""
    left: int = 0
    right: int = 0


@dataclass
class GameState:
    """Complete game state."""
    ball: Ball
    left_paddle: Paddle
    right_paddle: Paddle
    scores: Scores
    game_over: bool = False
    winner: str | None = None


@dataclass
class InputEvent:
    """Input event from keyboard."""
    key: str
    is_pressed: bool


@dataclass
class KeyState:
    """Current state of all relevant keys."""
    w: bool = False
    s: bool = False
    up: bool = False
    down: bool = False
