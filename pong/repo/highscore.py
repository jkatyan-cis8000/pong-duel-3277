"""Repository layer for high score persistence."""

import json
from pathlib import Path
from typing import Optional

from ..types import Scores


SCORE_FILE = Path.home() / '.pong_highscore.json'


def load_high_score() -> Scores:
    """Load high scores from file."""
    if not SCORE_FILE.exists():
        return Scores()
    try:
        with open(SCORE_FILE, 'r') as f:
            data = json.load(f)
            return Scores(left=data.get('left', 0), right=data.get('right', 0))
    except (json.JSONDecodeError, IOError):
        return Scores()


def save_high_score(scores: Scores) -> None:
    """Save high scores to file."""
    try:
        SCORE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SCORE_FILE, 'w') as f:
            json.dump({'left': scores.left, 'right': scores.right}, f)
    except IOError:
        pass  # Fail silently if we can't save


def update_high_score(current: Scores, new: Scores) -> bool:
    """Update high score if new scores are higher."""
    updated = False
    if new.left > current.left:
        current.left = new.left
        updated = True
    if new.right > current.right:
        current.right = new.right
        updated = True
    if updated:
        save_high_score(current)
    return updated
