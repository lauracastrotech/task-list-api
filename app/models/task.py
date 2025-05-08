from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
# from datetime import datetime
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[bool]] = mapped_column(nullable=True)
    
    def to_dict(self):
        return {
                "id":self.id,
                "title":self.title,
                "description":self.description,
                "completed_at": self.completed_at 
            }
        
        # task_dict = {
        #     "id": self.id,
        #     "title": self.title,
        #     "description": self.description,
        #     "is_complete": self.completed_at,
        # }
        # return task_dict
    
    # def to_dict(self, include_completed_at=False):
    #     task_dict = {
    #         "id": self.id,
    #         "title": self.title,
    #         "description": self.description,
    #         "is_complete": bool(self.completed_at),
    #     }
    #     if include_completed_at:
    #         task_dict["completed_at"] = self.completed_at
    #     return task_dict

    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data["completed_at"]
        )
