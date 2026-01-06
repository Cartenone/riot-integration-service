from pydantic import BaseModel

class PlayerLookupRequest(BaseModel):
    regional: str      # EUW1
    platform: str      # EUROPE
    game_name: str
    tag_line: str
    force_refresh: bool = False
