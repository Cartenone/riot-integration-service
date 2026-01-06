from sqlalchemy import String, Integer, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class MatchParticipant(Base):
    __tablename__ = "match_participants"
    __table_args__ = (UniqueConstraint("match_id", "puuid", name="uq_match_participant"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    match_id: Mapped[str] = mapped_column(
        String(32),
        ForeignKey("matches.match_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    puuid: Mapped[str] = mapped_column(String(90), nullable=False, index=True)

    game_name: Mapped[str | None] = mapped_column(String(40), nullable=True)
    tag_line: Mapped[str | None] = mapped_column(String(10), nullable=True)

    champion_name: Mapped[str | None] = mapped_column(String(40), nullable=True)
    win: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    kills: Mapped[int | None] = mapped_column(Integer, nullable=True)
    deaths: Mapped[int | None] = mapped_column(Integer, nullable=True)
    assists: Mapped[int | None] = mapped_column(Integer, nullable=True)
