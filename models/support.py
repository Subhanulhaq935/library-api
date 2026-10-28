
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Numeric,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship

from core.database import Base


class Support(Base):
    __tablename__ = "supports"

    id = Column(Integer, primary_key=True, index=True)

    work_id = Column(
        Integer,
        ForeignKey("works.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    supporter_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    amount = Column(Numeric(10, 2), nullable=False)

    supported_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    supporter = relationship("User", back_populates="supports")
    work = relationship("Work", back_populates="supports")
