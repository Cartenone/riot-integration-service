from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    region: Mapped[str] = mapped_column(String(10), nullable=False)
    platform: Mapped[str] = mapped_column(String(15), nullable=False)
    summoner_name: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)

    puuid: Mapped[str] = mapped_column(String(90), nullable=False, unique=True, index=True)
    summoner_id: Mapped[str | None] = mapped_column(String(90), nullable=True)


    last_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )
