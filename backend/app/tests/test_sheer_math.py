import pytest
from app.engines.curtain_math import fabric_meters
from app.modules.sheer_layer import sheer_meters


def test_sheer_seeded():
    r = sheer_meters(3.0, 2.6, 2.0, 0.08, 0.12, 2.8)
    assert r == fabric_meters(3.0, 2.6, 2.0, 0.08, 0.12, 2.8)
    assert r["finished_width"] == 6.0
    assert r["panels"] == 3
    assert r["cut_height"] == 2.8
    assert r["meters"] == 8.4


def test_sheer_single_panel_narrow():
    assert sheer_meters(1.0, 2.0, 1.5, 0.0, 0.0, 2.8)["panels"] == 1


def test_sheer_zero_width_fails():
    with pytest.raises(ValueError, match="fabric width required"):
        sheer_meters(3.0, 2.6, 2.0, 0.08, 0.12, 0.0)
