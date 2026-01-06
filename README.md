# Riot Integration Service (FastAPI)

Backend service that integrates Riot Games APIs to:
- lookup players by Riot ID (gameName + tagLine)
- import match history by PUUID
- persist matches and participants into PostgreSQL
- manage schema changes with Alembic migrations

## Tech Stack
- Python, FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Alembic migrations
- httpx (Riot API client)

