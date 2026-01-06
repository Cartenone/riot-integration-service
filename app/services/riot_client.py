import os
import httpx
from dotenv import load_dotenv

load_dotenv()
RIOT_API_KEY = os.getenv("RIOT_API_KEY")
if not RIOT_API_KEY:
    raise RuntimeError("RIOT_API_KEY not set")

REGIONAL_BASE = {
    "EUROPE": "https://europe.api.riotgames.com",
    "AMERICAS": "https://americas.api.riotgames.com",
    "ASIA": "https://asia.api.riotgames.com",
}

PLATFORM_BASE = {
    "EUW1": "https://euw1.api.riotgames.com",
    "EUN1": "https://eun1.api.riotgames.com",
    "NA1": "https://na1.api.riotgames.com",
    "KR": "https://kr.api.riotgames.com",
}

def get_summoner_by_name(regional: str, game_name: str, tag_line: str) -> dict:
    regional = regional.upper()
    if regional not in REGIONAL_BASE:
        raise ValueError(f"Unsupported regional routing: {regional}")

    url = f"{REGIONAL_BASE[regional]}/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    headers = {"X-Riot-Token": RIOT_API_KEY}

    with httpx.Client(timeout=10.0) as client:
        r = client.get(url, headers=headers)

    if r.status_code == 404:
        return {"_not_found": True}
    r.raise_for_status()
    return r.json()

def get_account_by_puuid(regional: str, puuid: str) -> dict:
    regional = regional.upper()
    if regional not in REGIONAL_BASE:
        raise ValueError(f"Unsupported regional routing: {regional}")

    url = f"{REGIONAL_BASE[regional]}/riot/account/v1/accounts/by-puuid/{puuid}"
    headers = {"X-Riot-Token": RIOT_API_KEY}

    with httpx.Client(timeout=10.0) as client:
        r = client.get(url, headers=headers)

    if r.status_code == 404:
        return {"_not_found": True}
    r.raise_for_status()
    return r.json()

def get_match_ids_by_puuid(regional: str, puuid: str, start: int = 0, count: int = 20) -> list[str]:
    regional = regional.upper()
    if regional not in REGIONAL_BASE:
        raise ValueError(f"Unsupported regional routing: {regional}")

    url = f"{REGIONAL_BASE[regional]}/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}"
    headers = {"X-Riot-Token": RIOT_API_KEY}

    with httpx.Client(timeout=10.0) as client:
        r = client.get(url, headers=headers)

    if r.status_code == 404:
        return []
    r.raise_for_status()
    return r.json()

def get_match_detail(regional: str, match_id: str) -> dict:
    regional = regional.upper()
    if regional not in REGIONAL_BASE:
        raise ValueError(f"Unsupported regional routing: {regional}")

    url = f"{REGIONAL_BASE[regional]}/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": RIOT_API_KEY}

    with httpx.Client(timeout=10.0) as client:
        r = client.get(url, headers=headers)

    if r.status_code == 404:
        return {"_not_found": True}
    r.raise_for_status()
    return r.json()
