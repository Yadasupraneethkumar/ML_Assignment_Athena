from fastapi import APIRouter
from pydantic import BaseModel
from puzzles.generator import PuzzleEngine

router = APIRouter()


@router.get("/")
def get_puzzle():
    return PuzzleEngine.generate()


class PuzzleCheckRequest(BaseModel):
    user_answer: str
    correct: str


@router.post("/check")
def check_puzzle(payload: PuzzleCheckRequest):
    user_answer = payload.user_answer
    correct = payload.correct

    return {
        "user_answer": user_answer,
        "correct_answer": correct,
        "is_correct": str(user_answer).strip() == str(correct).strip()
    }
