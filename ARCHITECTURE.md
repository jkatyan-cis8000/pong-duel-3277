# Pong Game Architecture

## Overview

This is a two-player Pong game built with a layered architecture. Each player controls a vertical paddle (left player uses 'W'/'S', right player uses 'Up'/'Down' arrow keys) to bounce a ball back and forth.

## Architecture

### Layers

| Layer       | Responsibility                                            |
|-------------|-----------------------------------------------------------|
| `types`     | Core data models: Ball, Paddle, Position, GameState     |
| `config`    | Constants: screen size, paddle speed, ball speed, win score |
| `repo`      | Persistence layer (high score storage)                  |
| `service`   | Business logic: movement, collision detection, scoring  |
| `runtime`   | Application orchestration and event loop                 |
| `ui`        | CLI rendering of game state                              |
| `providers` | Input handling (keyboard) and output (terminal display) |

### Module Breakdown

#### `src/types/`
- `ball.py`: Ball model with position and velocity
- `paddle.py`: Paddle model with position and dimensions
- `game_state.py`: Complete game state including scores
- `input.py`: Input events (key presses)

#### `src/config/`
- `settings.py`: Game constants (dimensions, speeds, win threshold)
- `keys.py`: Key binding constants

#### `src/repo/`
- `highscore.py`: High score persistence

#### `src/service/`
- `ball.py`: Ball movement and collision logic
- `paddle.py`: Paddle movement logic
- `game.py`: Main game loop and state transitions

#### `src/runtime/`
- `main.py`: Entry point and app lifecycle
- `event_loop.py`: Game event processing

#### `src/ui/`
- `renderer.py`: CLI rendering of game board
- `display.py`: Score display and messages

#### `src/providers/`
- `input.py`: Keyboard input reading
- `display.py`: Terminal output rendering

### Data Flow

```
Input (keyboard) → providers/input.py → service/paddle.py
                                   → types/input.py
                                  
Game Loop (runtime/event_loop.py) → service/game.py
                                   → service/ball.py
                                   → service/paddle.py
                                  
State → ui/renderer.py → providers/display.py → Terminal
```

### Winning Condition

Game ends when a player reaches `WIN_SCORE` (configurable, default 5).

### Reset Logic

After each point, the ball resets to center with random direction.
