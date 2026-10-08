# Clock Face Display

Renders a digital clock face string from an epoch timestamp and optional timezone offset, using block characters for fixed-width output.

```python
from clock_face_display import render_clock, ClockFaceRenderer

print(render_clock(0, tz_offset_minutes=0))
# 00:00 UTC, rendered as a 5-line block-character display

r = ClockFaceRenderer(tz_offset_minutes=330)
print(r.render(0))
# 05:30 in UTC+5:30
```

## Why

Terminal widgets and log headers that show a time often use `strftime` and get variable-width output because `1` is narrower than `0` in most fonts. This library renders each digit as a fixed 6-column block so the display never shifts width when the minute changes. The trade-off is size: each clock face is five lines tall and roughly thirty-four characters wide, which is fine for a dashboard panel and wrong for a one-line log stamp.

## Edge cases

The timezone offset is given in **minutes**, not hours, so half-hour zones like India (+330) work without floating point. Negative epoch timestamps are rejected and raise `ValueError`; the library is intended for live clocks, not historical dates before 1970. `NaN` and `inf` are also rejected. Seconds are not displayed — the face shows `HH:MM` only, because a display that updates every second is noisy in a terminal.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

