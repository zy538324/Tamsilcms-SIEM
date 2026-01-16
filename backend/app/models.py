from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    hostname: Mapped[str] = mapped_column(String(255))
    os_type: Mapped[str] = mapped_column(String(50))
    os_version: Mapped[str] = mapped_column(String(100))
    api_key_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[str] = mapped_column(DateTime(timezone=False), server_default=func.now())


class LogEntry(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    agent_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("agents.id"))
    log_source: Mapped[str] = mapped_column(String(255))
    event_time: Mapped[str] = mapped_column(DateTime(timezone=False))
    received_at: Mapped[str] = mapped_column(DateTime(timezone=False), server_default=func.now())
    event_level: Mapped[str] = mapped_column(String(20))
    event_id: Mapped[str] = mapped_column(String(50))
    message: Mapped[str] = mapped_column(Text)
