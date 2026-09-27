from fastapi import HTTPException
from app.engines.curtain_math import fabric_meters
from app.modules.sheer_layer import sheer_meters
from app.repositories import fabrics, history, settings_repo, windows

def _resolve_fullness(w, settings):
    return float(w.get("fullness") or settings.get("default_fullness", 2.0))

def run_estimate(window_id: int, fabric_id: int, save: bool, note: str,
                 sheer_on: bool = False, sheer_fabric_id: int | None = None,
                 sheer_fullness: float | None = None):
    w = windows.get_window(window_id)
    f = fabrics.get_fabric(fabric_id)
    if not w or not f:
        raise HTTPException(404, "not found")
    if w.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty window")
    if f.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty fabric")
    settings = settings_repo.get_all()
    fullness = _resolve_fullness(w, settings)
    sf = None
    sfull = None
    if sheer_on:
        if sheer_fabric_id is None:
            raise HTTPException(422, "sheer fabric required")
        sf = fabrics.get_fabric(sheer_fabric_id)
        if not sf:
            raise HTTPException(404, "not found")
        if sf.get("data_quality") == "dirty":
            raise HTTPException(422, "dirty fabric")
        sfull = float(sheer_fullness) if sheer_fullness is not None else _resolve_fullness(w, settings)
        if sfull <= 0:
            raise HTTPException(422, "sheer fullness must be positive")
    try:
        calc = fabric_meters(w["width"], w["height"], fullness, f["hem_top"], f["hem_bottom"], f["fabric_width"])
        scalc = sheer_meters(w["width"], w["height"], sfull, sf["hem_top"], sf["hem_bottom"], sf["fabric_width"]) if sf else None
    except ValueError as e:
        raise HTTPException(422, str(e))
    result = {**calc}
    if scalc is not None:
        result["sheer"] = {"fabric_id": sf["id"], "fabric_name": sf["name"], "fullness": sfull, **scalc}
    run_id = history.insert_run(window_id, fabric_id, result, note) if save else None
    return {"window": w, "fabric": f, "run_id": run_id, **result}
