from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from sqlalchemy import ForeignKey
from datetime import datetime
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from .goal import Goal

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")
    
    def to_dict(self):
        task = {
                "id":self.id,
                "title":self.title,
                "description":self.description,
                "is_complete": self.is_complete()
            }
        if self.goal_id:
            task["goal_id"] =  self.goal_id
        return task
    
    def is_complete(self):
        return self.completed_at is not None
    
    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data.get("completed_at")
        )
