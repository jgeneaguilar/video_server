import bcrypt
from sqlalchemy import Column, Text, DateTime
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .meta import Base


class User(Base):
    """A user model"""

    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(Text, nullable=False, unique=True)
    password_hash = Column(Text)
    mobile_token = Column(Text)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    rooms = relationship("Room", secondary="room_memberships", back_populates="users")

    def __init__(self, **kwargs):
        if "password" in kwargs:
            self.set_password(kwargs.pop("password"))
        # map the rest of Column names to class attributes
        super(User, self).__init__(**kwargs)

    def set_password(self, pw):
        pwhash = bcrypt.hashpw(pw.encode("utf8"), bcrypt.gensalt())
        self.password_hash = pwhash.decode("utf8")

    def check_password(self, pw):
        if self.password_hash is not None:
            expected_hash = self.password_hash.encode("utf8")
            return bcrypt.checkpw(pw.encode("utf8"), expected_hash)
        return False
