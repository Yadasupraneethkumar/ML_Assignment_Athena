from fastapi import APIRouter
from pydantic import BaseModel
from api.deps import uc, SYSTEMS

router = APIRouter()


class ExplainRequest(BaseModel):
    source: str
    target: str
    value: str


@router.post("/")
def explain(payload: ExplainRequest):
    src = payload.source.lower()
    dst = payload.target.lower()
    value = payload.value

    if src not in SYSTEMS or dst not in SYSTEMS:
        return {"error": f"Unsupported numeral system: {src} or {dst}"}

    try:
        result, steps = uc.explain(src, dst, value)
        return {
            "input": value,
            "source_system": src,
            "target_system": dst,
            "result": result,
            "steps": steps
        }
    except Exception as e:
        return {"error": str(e)}
