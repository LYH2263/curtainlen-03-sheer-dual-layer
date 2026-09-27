from pydantic import BaseModel

class EstimateRequest(BaseModel):
    window_id: int
    fabric_id: int
    save: bool = False
    note: str = ""
    sheer_on: bool = False
    sheer_fabric_id: int | None = None
    sheer_fullness: float | None = None
