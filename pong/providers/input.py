"""Provider layer for input handling."""

import sys
import termios
import tty
from pong.types import InputEvent


class InputProvider:
    """Provides keyboard input events."""
    
    def __init__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
    
    def __enter__(self):
        tty.setcbreak(self.fd)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
    
    def poll(self) -> list[InputEvent]:
        """Poll for input events. Returns list of key events."""
        import select
        
        events = []
        
        if select.select([sys.stdin], [], [], 0)[0]:
            key = sys.stdin.read(1)
            
            # Handle escape sequences for arrow keys
            if key == '\x1b':  # ESC
                next1 = sys.stdin.read(1)
                next2 = sys.stdin.read(1)
                if next1 == '[' and next2 == 'A':
                    events.append(InputEvent(key='up', is_pressed=True))
                elif next1 == '[' and next2 == 'B':
                    events.append(InputEvent(key='down', is_pressed=True))
            elif key in '\r\n':
                events.append(InputEvent(key='enter', is_pressed=True))
            else:
                events.append(InputEvent(key=key, is_pressed=True))
        
        return events
