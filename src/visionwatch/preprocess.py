"""Small, deterministic OpenCV preparation stage for screen text."""

from __future__ import annotations

import cv2
import numpy as np


def prepare_for_ocr(image: np.ndarray, scale: float = 1.8) -> np.ndarray:
    if image.size == 0:
        raise ValueError("The capture is empty")
    if scale < 1.0 or scale > 4.0:
        raise ValueError("OCR scale must be between 1.0 and 4.0")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image.copy()
    enlarged = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    # Bilateral filtering reduces compression noise while keeping character
    # edges sharper than a plain blur would.
    denoised = cv2.bilateralFilter(enlarged, 7, 35, 35)

    # CLAHE corrects local contrast, which helps when the watched application
    # contains gradients, shadows or uneven panel brightness.
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(denoised)
