import bcrypt
from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql.expression import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .meta import Base


class UserModel(Base):
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

    def set_password(self, pw):
        pwhash = bcrypt.hashpw(pw.encode("utf8"), bcrypt.gensalt())
        self.password_hash = pwhash.decode("utf8")

    def check_password(self, pw):
        if self.password_hash is not None:
            expected_hash = self.password_hash.encode("utf8")
            return bcrypt.checkpw(pw.encode("utf8"), expected_hash)
        return False
