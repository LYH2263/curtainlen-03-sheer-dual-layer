"""sheer layer: same panel geometry as the main fabric, with sheer inputs."""
from app.engines.curtain_math import fabric_meters


def sheer_meters(
    window_w: float,
    window_h: float,
    fullness: float,
    hem_top: float,
    hem_bottom: float,
    fabric_width: float,
) -> dict:
    return fabric_meters(window_w, window_h, fullness, hem_top, hem_bottom, fabric_width)
