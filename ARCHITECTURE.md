# Architecture

```text
Windows window A ─┐
                  ├─► MSS capture ─► OpenCV preparation ─► OCR
Windows window B ─┘                                      │
                                                         ▼
                                            value + confidence filter
                                                         │
                                                         ▼
                                        safe formula + fresh-data tracker
                                                         │
                                      ┌──────────────────┼──────────────┐
                                      ▼                  ▼              ▼
                                  visual alert          sound       event history
```

Each source has its own last-reading state. This avoids repeated alarms for a
static value without incorrectly treating the same value in a second
application as old.

All recognition happens locally. The complete application binds its UI bridge
to loopback only and writes event history to the operating system's application
data location.

## Decision boundary

Only readings above the confidence threshold reach the rule evaluator. An alert
is emitted when that rule matches a fresh value for the current source.
