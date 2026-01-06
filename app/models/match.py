from datetime import datetime
from sqlalchemy import String, Integer, DateTime, UniqueConstraint, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (UniqueConstraint("match_id", name="uq_matches_match_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    match_id: Mapped[str] = mapped_column(String(32), nullable=False, index=True)  # EUW1_...
    regional: Mapped[str] = mapped_column(String(10), nullable=False)
    platform: Mapped[str] = mapped_column(String(10), nullable=False)

    game_start_ms: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    queue_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
