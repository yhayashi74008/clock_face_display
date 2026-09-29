import unittest

from clock_face_display import render_clock, ClockFaceRenderer


class TestRenderClock(unittest.TestCase):
    def test_midnight_utc(self):
        # 1970-01-01 00:00:00 UTC
        out = render_clock(0)
        lines = out.split("\n")
        self.assertEqual(len(lines), 5)
        # Each digit block is 6 chars wide, plus 1 space separator.
        # "00:00" -> 4 digits + 1 colon = 5 blocks.
        # Max line width is 6*5 + 4 (separators) = 34, but trailing
        # spaces are stripped so we check the top row which is full.
        self.assertEqual(len(lines[0]), 34)
        self.assertIn("██████", lines[0])

    def test_known_time(self):
        # 2023-01-01 12:34:00 UTC
        # epoch for that moment:
        import datetime as dt
        ts = int(dt.datetime(2023, 1, 1, 12, 34, 0, tzinfo=dt.timezone.utc).timestamp())
        out = render_clock(ts)
        lines = out.split("\n")
        # Top row of "1" is right-aligned block, then '2' is full.
        # "12:34" -> '1' top row is "    ██", then '2' top row is "██████".
        self.assertTrue(lines[0].startswith("    ██ ██████"))

    def test_positive_offset(self):
        # 00:00 UTC + 60 min = 01:00
        out = render_clock(0, tz_offset_minutes=60)
        lines = out.split("\n")
        # "01:00" - '0' top row is full block.
        self.assertTrue(lines[0].startswith("██████"))

    def test_negative_offset(self):
        # 00:30 UTC - 60 min = 23:30 previous day
        import datetime as dt
        ts = int(dt.datetime(1970, 1, 1, 0, 30, 0, tzinfo=dt.timezone.utc).timestamp())
        out = render_clock(ts, tz_offset_minutes=-60)
        lines = out.split("\n")
        # "23:30" - top row of '2' is full block.
        self.assertTrue(lines[0].startswith("██████"))

    def test_half_hour_offset(self):
        # India is UTC+5:30. 00:00 UTC -> 05:30 IST.
        out = render_clock(0, tz_offset_minutes=330)
        lines = out.split("\n")
        # "05:30" - '0' top row is full.
        self.assertTrue(lines[0].startswith("██████"))

    def test_fixed_width_all_digits(self):
        # Every minute in a 24-hour cycle should produce 5 lines.
        # We can't test all 1440 cheaply, but sample a few.
        for mins in range(0, 1440, 60):
            ts = mins * 60
            out = render_clock(ts)
            lines = out.split("\n")
            self.assertEqual(len(lines), 5, f"failed at {mins} minutes")

    def test_negative_epoch_raises(self):
        with self.assertRaises(ValueError):
            render_clock(-1)

    def test_nan_raises(self):
        with self.assertRaises(ValueError):
            render_clock(float("nan"))

    def test_inf_raises(self):
        with self.assertRaises(ValueError):
            render_clock(float("inf"))

    def test_output_is_str(self):
        out = render_clock(0)
        self.assertIsInstance(out, str)


class TestClockFaceRenderer(unittest.TestCase):
    def test_holds_offset(self):
        r = ClockFaceRenderer(tz_offset_minutes=120)
        self.assertEqual(r.tz_offset_minutes, 120)

    def test_render_uses_offset(self):
        # 00:00 UTC + 120 min = 02:00
        r = ClockFaceRenderer(tz_offset_minutes=120)
        out = r.render(0)
        lines = out.split("\n")
        # "02:00" - '0' top row full.
        self.assertTrue(lines[0].startswith("██████"))

    def test_default_offset_zero(self):
        r = ClockFaceRenderer()
        self.assertEqual(r.tz_offset_minutes, 0)


if __name__ == "__main__":
    unittest.main()
