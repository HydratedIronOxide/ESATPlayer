import time

class Stopwatch:
    """A pause-aware stopwatch whose result never depends on GUI refresh rate."""

    def __init__(self) -> None:
        self.running = False
        self.accumulated = 0.0
        self.started_at = 0.0

    def start(self) -> None:
        if not self.running:
            self.started_at = time.perf_counter()
            self.running = True

    def pause(self) -> None:
        if self.running:
            self.accumulated += time.perf_counter() - self.started_at
            self.running = False

    def reset(self) -> None:
        self.running = False
        self.accumulated = 0.0
        self.started_at = 0.0

    def elapsed(self) -> float:
        return self.accumulated + (time.perf_counter() - self.started_at if self.running else 0.0)

    @staticmethod
    def format_seconds(second: float) -> str:
        """Return a compact minutes-and-seconds representation."""
        second = max(0.0, second)
        minutes = int(second // 60)
        remainder = second - minutes * 60
        return f"{minutes}:{remainder:.1f}" if minutes else f"{remainder:.1f}s"







