from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from app.db.session import get_db
from app.models.player import Player
from app.models.player_riot_id import PlayerRiotId
from app.models.match import Match
from app.models.match_participant import MatchParticipant
from app.services.riot_client import get_match_ids_by_puuid, get_match_detail

router = APIRouter(prefix="/matches", tags=["matches"])


@router.post("/import/by-puuid/{puuid}")
def import_matches_by_puuid(puuid: str, count: int = 20, db: Session = Depends(get_db)):
    # 1) player must exist
    player = db.query(Player).filter(Player.puuid == puuid).one_or_none()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found. Run /players/lookup first.")

    # ✅ standard deciso:
    # - player.region = EUROPE (regional routing)
    # - player.platform = EUW1 (platform shard)
    regional = (player.region or "").upper()
    platform = (player.platform or "").upper()

    if not regional or not platform:
        raise HTTPException(status_code=400, detail="Player missing region/platform. Re-run /players/lookup.")

    # 2) get match ids (match-v5 usa REGIONAL routing)
    match_ids = get_match_ids_by_puuid(regional, puuid, start=0, count=count)
    if not match_ids:
        return {"requested": 0, "new_match_ids": 0, "inserted_matches": 0, "inserted_participants": 0}

    # 3) avoid duplicates (matches già presenti)
    existing = set(mid for (mid,) in db.query(Match.match_id).filter(Match.match_id.in_(match_ids)).all())
    new_match_ids = [mid for mid in match_ids if mid not in existing]

    inserted_matches = 0
    inserted_participants = 0
    now = datetime.now(timezone.utc)

    for mid in new_match_ids:
        detail = get_match_detail(regional, mid)
        if detail.get("_not_found"):
            continue

        info = detail.get("info", {})
        metadata = detail.get("metadata", {})
        match_id = metadata.get("matchId", mid)

        # 3a) insert match header (ON CONFLICT DO NOTHING)
        match_row = {
            "match_id": match_id,
            "regional": regional,   # EUROPE
            "platform": platform,  # EUW1
            "game_start_ms": info.get("gameStartTimestamp"),
            "queue_id": info.get("queueId"),
            "created_at": now,
        }

        stmt_m = insert(Match).values(match_row).on_conflict_do_nothing(
            constraint="uq_matches_match_id"
        )
        res_m = db.execute(stmt_m)
        if res_m.rowcount:
            inserted_matches += 1

        participants = info.get("participants", []) or []
        if not participants:
            continue

        # 3b) UPSERT/SEED players (tutti i puuid del match)
        player_rows = []
        riot_id_rows = []
        part_rows = []

        for p in participants:
            p_puuid = p.get("puuid")
            if not p_puuid:
                continue

            gname = p.get("riotIdGameName")
            tline = p.get("riotIdTagline")

            player_rows.append({
                "puuid": p_puuid,
                "region": regional,     # EUROPE
                "platform": platform,   # EUW1
                "summoner_name": gname, # opzionale
                "summoner_id": None,
                "last_updated": now,
            })

            if gname and tline:
                riot_id_rows.append({
                    "puuid": p_puuid,
                    "game_name": gname,
                    "tag_line": tline,
                    "first_seen_at": now,
                    "last_seen_at": now,
                })

            part_rows.append({
                "match_id": match_id,
                "puuid": p_puuid,
                "game_name": gname,
                "tag_line": tline,
                "champion_name": p.get("championName"),
                "win": p.get("win"),
                "kills": p.get("kills"),
                "deaths": p.get("deaths"),
                "assists": p.get("assists"),
            })

        # seed players: DO NOTHING se esiste già (puuid UNIQUE)
        if player_rows:
            stmt_p = insert(Player).values(player_rows).on_conflict_do_nothing(
                index_elements=["puuid"]
            )
            db.execute(stmt_p)

        # riot id history: se esiste aggiorno last_seen_at
        if riot_id_rows:
            stmt_r = insert(PlayerRiotId).values(riot_id_rows).on_conflict_do_update(
                constraint="uq_player_riot_id",
                set_={"last_seen_at": now},
            )
            db.execute(stmt_r)

        # match participants: DO NOTHING su (match_id, puuid)
        if part_rows:
            stmt_mp = insert(MatchParticipant).values(part_rows).on_conflict_do_nothing(
                constraint="uq_match_participant"
            )
            res_mp = db.execute(stmt_mp)
            inserted_participants += res_mp.rowcount or 0

    db.commit()
    return {
        "requested": len(match_ids),
        "new_match_ids": len(new_match_ids),
        "inserted_matches": inserted_matches,
        "inserted_participants": inserted_participants,
    }
