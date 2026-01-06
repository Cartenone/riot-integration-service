from datetime import datetime, timezone
from sqlalchemy import String, DateTime, ForeignKey, UniqueConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class PlayerRiotId(Base):
    __tablename__ = "player_riot_ids"
    __table_args__ = (
        UniqueConstraint("puuid", "game_name", "tag_line", name="uq_player_riot_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    puuid: Mapped[str] = mapped_column(
        String(90),
        ForeignKey("players.puuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    game_name: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    tag_line: Mapped[str] = mapped_column(String(10), nullable=False, index=True)

    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
