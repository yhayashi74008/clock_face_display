from __future__ import annotations

import datetime as _dt
import math


_DIGITS = {
    '0': [
        "██████",
        "██  ██",
        "██  ██",
        "██  ██",
        "██████",
    ],
    '1': [
        "    ██",
        "    ██",
        "    ██",
        "    ██",
        "    ██",
    ],
    '2': [
        "██████",
        "    ██",
        "██████",
        "██    ",
        "██████",
    ],
    '3': [
        "██████",
        "    ██",
        "██████",
        "    ██",
        "██████",
    ],
    '4': [
        "██  ██",
        "██  ██",
        "██████",
        "    ██",
        "    ██",
    ],
    '5': [
        "██████",
        "██    ",
        "██████",
        "    ██",
        "██████",
    ],
    '6': [
        "██████",
        "██    ",
        "██████",
        "██  ██",
        "██████",
    ],
    '7': [
        "██████",
        "    ██",
        "    ██",
        "    ██",
        "    ██",
    ],
    '8': [
        "██████",
        "██  ██",
        "██████",
        "██  ██",
        "██████",
    ],
    '9': [
        "██████",
        "██  ██",
        "██████",
        "    ██",
        "██████",
    ],
}

_COLON = [
    "      ",
    "  ██  ",
    "      ",
    "  ██  ",
    "      ",
]


def _block_for_char(ch: str) -> list[str]:
    if ch == ':':
        return _COLON
    return _DIGITS[ch]


def render_clock(epoch_seconds: float, tz_offset_minutes: int = 0) -> str:
    """Render an HH:MM digital clock face from an epoch timestamp.

    Uses fixed-width block characters so the output is the same width
    regardless of which digits appear. The timezone offset is given in
    minutes so both whole-hour and half-hour offsets (e.g. India, +330)
    work without floating point.

    The clock displays HH:MM in 24-hour format. Seconds are dropped on
    purpose: a clock face that flickers every second is noisy in a
    terminal log, and the minute resolution is what matters for a
    display widget.
    """
    if not math.isfinite(epoch_seconds):
        raise ValueError("epoch_seconds must be a finite number")
    if epoch_seconds < 0:
        raise ValueError("epoch_seconds must be non-negative")

    dt = _dt.datetime.fromtimestamp(epoch_seconds, tz=_dt.timezone.utc)
    if tz_offset_minutes:
        dt = dt.astimezone(_dt.timezone(_dt.timedelta(minutes=tz_offset_minutes)))

    time_str = dt.strftime("%H:%M")

    rows = ["" for _ in range(5)]
    for ch in time_str:
        block = _block_for_char(ch)
        for i in range(5):
            rows[i] += block[i] + " "

    return "\n".join(row.rstrip() for row in rows)


class ClockFaceRenderer:
    """Stateful renderer that holds a timezone offset.

    Exists so callers passing the same offset repeatedly don't have to
    thread it through every call site. The offset is fixed at
    construction; if you need to change it, make a new renderer.
    """

    def __init__(self, tz_offset_minutes: int = 0):
        self.tz_offset_minutes = tz_offset_minutes

    def render(self, epoch_seconds: float) -> str:
        return render_clock(epoch_seconds, self.tz_offset_minutes)
