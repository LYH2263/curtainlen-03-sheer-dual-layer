import pytest
from fastapi import HTTPException
import app.db as db
from app.repositories import history
from app.services.estimate_service import run_estimate


def _count():
    c = db.connect()
    try:
        return c.execute("SELECT COUNT(*) c FROM calc_runs").fetchone()["c"]
    finally:
        c.close()


def test_no_sheer_equivalence(tmp_db):
    before = _count()
    r = run_estimate(1, 1, False, "")
    assert r["run_id"] is None
    assert "sheer" not in r
    assert r["finished_width"] == 6.0
    assert r["panels"] == 5
    assert r["cut_height"] == 2.85
    assert r["meters"] == 14.25
    assert r["fabric_width"] == 1.4
    assert _count() == before


def test_sheer_on_dry(tmp_db):
    before = _count()
    r = run_estimate(1, 1, False, "", sheer_on=True, sheer_fabric_id=2, sheer_fullness=2.0)
    assert r["panels"] == 5 and r["meters"] == 14.25
    s = r["sheer"]
    assert s["fabric_id"] == 2
    assert s["fabric_name"] == "纱帘2.8m"
    assert s["fullness"] == 2.0
    assert s["finished_width"] == 6.0
    assert s["panels"] == 3
    assert s["cut_height"] == 2.8
    assert s["meters"] == 8.4
    assert s["fabric_width"] == 2.8
    assert _count() == before


def test_sheer_fullness_defaults_to_window(tmp_db):
    r = run_estimate(2, 2, False, "", sheer_on=True, sheer_fabric_id=2)
    assert r["sheer"]["fullness"] == 2.0


@pytest.mark.parametrize("bad", [0, -1])
def test_sheer_fullness_nonpositive(tmp_db, bad):
    before = _count()
    with pytest.raises(HTTPException) as ei:
        run_estimate(1, 1, False, "", sheer_on=True, sheer_fabric_id=2, sheer_fullness=bad)
    assert ei.value.status_code == 422
    assert _count() == before


def test_sheer_dirty_zero_width_fabric(tmp_db):
    before = _count()
    with pytest.raises(HTTPException) as ei:
        run_estimate(1, 1, False, "", sheer_on=True, sheer_fabric_id=3, sheer_fullness=2.0)
    assert ei.value.status_code == 422
    assert _count() == before


def test_sheer_missing_fabric_id(tmp_db):
    before = _count()
    with pytest.raises(HTTPException) as ei:
        run_estimate(1, 1, False, "", sheer_on=True)
    assert ei.value.status_code == 422
    with pytest.raises(HTTPException) as ei2:
        run_estimate(1, 1, False, "", sheer_on=True, sheer_fabric_id=999, sheer_fullness=2.0)
    assert ei2.value.status_code == 404
    assert _count() == before


def test_dirty_main_fabric_fails(tmp_db):
    before = _count()
    with pytest.raises(HTTPException) as ei:
        run_estimate(1, 3, False, "")
    assert ei.value.status_code == 422
    assert _count() == before


def test_save_one_row_snapshot(tmp_db):
    before = _count()
    r = run_estimate(1, 1, True, "双层", sheer_on=True, sheer_fabric_id=2, sheer_fullness=2.0)
    assert r["run_id"] is not None
    assert _count() == before + 1
    saved = history.list_runs()[0]["result"]
    assert saved["panels"] == 5 and saved["meters"] == 14.25
    assert saved["sheer"]["panels"] == 3 and saved["sheer"]["meters"] == 8.4
    assert saved["sheer"]["fabric_name"] == "纱帘2.8m"
    r2 = run_estimate(1, 1, True, "单层")
    assert "sheer" not in history.list_runs()[0]["result"]
    assert _count() == before + 2
    assert r2["run_id"] != r["run_id"]


def test_snapshot_pinned_after_fabric_width_change(tmp_db):
    run_estimate(1, 1, True, "", sheer_on=True, sheer_fabric_id=2, sheer_fullness=2.0)
    before = history.list_runs()[0]["result"]
    c = db.connect()
    try:
        c.execute("UPDATE fabrics SET fabric_width=9.9 WHERE id IN (1,2)")
        c.commit()
    finally:
        c.close()
    after = history.list_runs()[0]["result"]
    assert after == before
    assert after["fabric_width"] == 1.4
    assert after["sheer"]["fabric_width"] == 2.8


def test_list_runs_window_filter(tmp_db):
    run_estimate(1, 1, True, "", sheer_on=True, sheer_fabric_id=2, sheer_fullness=2.0)
    run_estimate(2, 1, True, "")
    assert {r["window_id"] for r in history.list_runs()} == {1, 2}
    w1 = history.list_runs(window_id=1)
    assert len(w1) == 1 and w1[0]["window_id"] == 1
