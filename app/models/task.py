from app.core.config import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship 
from sqlalchemy import String, Integer, func, DateTime, ForeignKey
from datetime import datetime

class TasksOrm(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(64), index=True)
    description: Mapped[str] = mapped_column(String(2048))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now)

    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    owner = relationship("UsersOrm", back_populates="tasks")