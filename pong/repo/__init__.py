"""Repo module for Pong game."""

from .highscore import (
    load_high_score,
    save_high_score,
    update_high_score,
)

__all__ = [
    'load_high_score',
    'save_high_score',
    'update_high_score',
]
