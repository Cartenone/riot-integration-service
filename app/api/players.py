from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.models.player import Player
from app.schemas.lookup import PlayerLookupRequest
from app.services.riot_client import get_summoner_by_name

router = APIRouter(prefix="/players", tags=["players"])


@router.post("/lookup", status_code=status.HTTP_200_OK)
def lookup_player(payload: PlayerLookupRequest, db: Session = Depends(get_db)):

    account = get_summoner_by_name(
        payload.regional,
        payload.game_name,
        payload.tag_line,
    )

    if account.get("_not_found"):
        raise HTTPException(status_code=404, detail="Riot ID not found")

    puuid = account["puuid"]
    name = account.get("gameName") or payload.game_name
    now = datetime.now(timezone.utc)

    player = db.query(Player).filter(Player.puuid == puuid).one_or_none()

    if player is None:
        player = Player(
            region=payload.regional.upper(),      # EUROPE
            platform=payload.platform.upper(),    # EUW1
            summoner_name=name,
            puuid=puuid,
            summoner_id=None,
            last_updated=now,
        )
        db.add(player)
        db.commit()
        db.refresh(player)
    else:
        if payload.force_refresh:
            player.region = payload.regional.upper()      # EUROPE
            player.platform = payload.platform.upper()    # EUW1
            player.summoner_name = name
            player.last_updated = now
            db.commit()
            db.refresh(player)

    return {
        "id": player.id,
        "region": player.region,
        "platform": player.platform,
        "summoner_name": player.summoner_name,
        "puuid": player.puuid,
        "summoner_id": player.summoner_id,
        "last_updated": player.last_updated,
    }


@router.get("/by-name/{summoner_name}")
def get_players_by_name(summoner_name: str, db: Session = Depends(get_db)):
    players = (
        db.query(Player)
        .filter(func.lower(Player.summoner_name) == summoner_name.lower())
        .order_by(Player.last_updated.desc())
        .all()
    )

    if not players:
        raise HTTPException(status_code=404, detail="Player not found")

    return [
        {
            "id": p.id,
            "region": p.region,
            "platform": p.platform,
            "summoner_name": p.summoner_name,
            "puuid": p.puuid,
            "summoner_id": p.summoner_id,
            "last_updated": p.last_updated,
        }
        for p in players
    ]
