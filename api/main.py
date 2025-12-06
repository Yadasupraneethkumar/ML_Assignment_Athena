from fastapi import FastAPI
from .routes import convert, explain, puzzle

app = FastAPI(
    title="Universal Numeral Systems API",
    description="Convert, explain, and generate numeral system puzzles",
    version="1.0",
)

# Include routers with prefixes
app.include_router(convert.router, prefix="/convert", tags=["Convert"])
app.include_router(explain.router, prefix="/explain", tags=["Explain"])
app.include_router(puzzle.router, prefix="/puzzle", tags=["Puzzle"])


@app.get("/")
def root():
    return {"message": "Universal Numeral Systems API is running!"}
