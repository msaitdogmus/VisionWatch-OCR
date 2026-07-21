"""Source-aware duplicate suppression for OCR readings."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReadingDecision:
    source: str
    text: str
    is_fresh: bool
    formula_matched: bool
    alert_triggered: bool


class FreshReadingTracker:
    """Remember the last reading independently for every capture source."""

    def __init__(self) -> None:
        self._last_text: dict[str, str] = {}

    def classify(self, source: str, text: str, formula_matched: bool) -> ReadingDecision:
        previous = self._last_text.get(source)
        is_reading = bool(text.strip()) and text != "No text detected"
        is_fresh = is_reading and text != previous

        # Source A and Source B deliberately keep separate histories. A value
        # first seen in the second application is still a new event.
        self._last_text[source] = text
        return ReadingDecision(
            source=source,
            text=text,
            is_fresh=is_fresh,
            formula_matched=formula_matched,
            alert_triggered=formula_matched and is_fresh,
        )
