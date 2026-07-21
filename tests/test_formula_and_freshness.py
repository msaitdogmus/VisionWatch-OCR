import unittest

from visionwatch import FreshReadingTracker, SafeFormula


class FormulaAndFreshnessTests(unittest.TestCase):
    def test_customer_range_rule(self) -> None:
        self.assertTrue(SafeFormula.evaluate("x >= 100 and x < 200", 128.5))
        self.assertFalse(SafeFormula.evaluate("x < 0", 128.5))

    def test_function_calls_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            SafeFormula.evaluate("__import__('os')", 1)

    def test_duplicate_alert_is_suppressed_per_source(self) -> None:
        tracker = FreshReadingTracker()
        self.assertTrue(tracker.classify("Source A", "128.50", True).alert_triggered)
        self.assertFalse(tracker.classify("Source A", "128.50", True).alert_triggered)
        self.assertTrue(tracker.classify("Source B", "128.50", True).alert_triggered)


if __name__ == "__main__":
    unittest.main()
