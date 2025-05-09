from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .task import Task

class Goal(db.Model):

    # Add table dunder var and set to goal
    # The difference between having this or not, the table name itself is give the table a name, and hainvg it here gives us more control of the table being called. It allows us to define the name of the db table as opposed to the name to be automatically generated! This happens implicitly because it's a table dunder
    __tablename__ = "goal"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")
    
    def to_dict(self):
        return {
                "id":self.id,
                "title":self.title
            }
    
    @classmethod
    def from_dict(cls, goal_data):
        return cls(
            title=goal_data["title"]
        )