from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql.expression import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .meta import Base


class RoomMembership(Base):
    """An association table for rooms and users"""

    __tablename__ = "room_memberships"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE",),
        nullable=False,
    )
    room_id = Column(
        UUID(as_uuid=True),
        ForeignKey("rooms.id", onupdate="CASCADE", ondelete="CASCADE",),
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
