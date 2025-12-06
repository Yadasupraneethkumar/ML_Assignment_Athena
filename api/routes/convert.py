from fastapi import APIRouter
from pydantic import BaseModel
from api.deps import uc, SYSTEMS

router = APIRouter()


class ConvertRequest(BaseModel):
    source: str
    target: str
    value: str


@router.post("/")
def convert(payload: ConvertRequest):
    src = payload.source.lower()
    dst = payload.target.lower()
    value = payload.value

    if src not in SYSTEMS or dst not in SYSTEMS:
        return {"error": f"Unsupported numeral system: {src} or {dst}"}

    try:
        result = uc.convert(src, dst, value)
        return {
            "input": value,
            "source_system": src,
            "target_system": dst,
            "result": result
        }
    except Exception as e:
        return {"error": str(e)}
