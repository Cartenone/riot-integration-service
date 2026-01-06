from fastapi import FastAPI
from app.api.players import router as players_router
from app.api.matches import router as matches_router


app = FastAPI(title="Riot Integration Service")

app.include_router(players_router)
app.include_router(matches_router)

@app.get("/health")
def health():
    return {"status": "ok"}
