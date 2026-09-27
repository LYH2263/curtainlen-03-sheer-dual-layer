from fastapi import APIRouter
from app.repositories import history as repo
router = APIRouter()
@router.get("/runs")
def runs(limit: int = 50, window_id: int | None = None): return {"items": repo.list_runs(limit, window_id)}
