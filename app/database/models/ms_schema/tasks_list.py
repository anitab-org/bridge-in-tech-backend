from enum import unique, Enum
from datetime import date
from app.database.db_types.JsonCustomType import JsonCustomType
from app.database.sqlalchemy_extension import db


class TasksListModel(db.Model):
    """Model representation of a list of tasks.
    
    Attributes:
        id: Id of the list of tasks.
        tasks: A list of tasks, using JSON format.
        next_task_id: Id of the next task added to the list of tasks.
    """

    __tablename__ = "tasks_list"
    __table_args__ = {"schema": "public", "extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    tasks = db.Column(JsonCustomType)
    next_task_id = db.Column(db.Integer)

    def __init__(self, tasks: "TasksListModel" = None):
        """Initializes tasks.

        Args:
            tasks: A list of tasks.
        
        Raises:
            A Value Error if the task is not initialized.
        """

        if not tasks:
            self.tasks = []
            self.next_task_id = 1
        else:
            if isinstance(tasks, list):
                self.tasks = []
                self.next_task_id += 1
            else:
                raise TypeError("task is not initialized")

    def add_task(
        self, description: str, created_at: date, is_done=False, completed_at=None
    ) -> None:
        """Adds a task to the list of tasks.
        
        Args:
            description: A description of the task added.
            created_at: Date on which the task is created.
            is_done: Boolean specifying completion of the task.
            completed_at: Date on which task is completed.
        """

        task = {
            TasksFields.ID.value: self.next_task_id,
            TasksFields.DESCRIPTION.value: description,
            TasksFields.IS_DONE.value: is_done,
            TasksFields.CREATED_AT.value: created_at,
            TasksFields.COMPLETED_AT.value: completed_at,
        }
        self.next_task_id += 1
        self.tasks = self.tasks + [task]

    def delete_task(self, task_id: int) -> None:
        """Deletes a task from the list of tasks.

        Args:
            task_id: Id of the task to be deleted.
        """
        new_list = []
        for task in self.tasks:
            if task[TasksFields.ID.value] != task_id:
                new_list.append(task)

        self.tasks = new_list
        self.save_to_db()

    def update_task(
        self,
        task_id: int,
        description: str = None,
        is_done: bool = None,
        completed_at: date = None,
    ) -> None:
        """Updates a task.
        
        Args:
            task_id: Id of the task to be updated.
            description: A description of the task.
            created_at: Date on which the task is created.
            is_done: Boolean specifying completion of the task.
            completed_at: Date on which task is completed.
        """

        new_list = []
        for task in self.tasks:
            if task[TasksFields.ID.value] == task_id:
                new_task = task.copy()
                if not description:
                    new_task[TasksFields.DESCRIPTION.value] = description

                if not is_done:
                    new_task[TasksFields.IS_DONE.value] = is_done

                if not completed_at:
                    new_task[TasksFields.COMPLETED_AT.value] = completed_at

                new_list += [new_task]
                continue

            new_list += [task]

        self.tasks = new_list
        self.save_to_db()

    def find_task_by_id(self, task_id: int):
        """Returns the task that has the specified id.
        
        Args:
            task_id: Id of the task.

        Returns:
            The task instance.
        """
        task = list(
            filter(lambda task: task[TasksFields.ID.value] == task_id, self.tasks)
        )
        if not task:
            return None
        return task[0]

    def is_empty(self) -> bool:
        """Checks if the list of tasks is empty.

        Returns:
            Boolean; True if the task is empty, False otherwise.
        """

        return self.tasks

    def json(self):
        """Creates json object of the attributes of list of tasks.

        Returns:
            Json objects of attributes of list of tasks.
        """

        return {
            "id": self.id,
            "mentorship_relation_id": self.mentorship_relation_id,
            "tasks": self.tasks,
            "next_task_id": self.next_task_id,
        }

    def __repr__(self):
        """Creates a representation of an object.
        
        Returns:
            A string representation of the task object.
        """

        return (
            f"Task id is {self.id}\n"
            f"Tasks list is {self.tasks}\n"
            f"Next task id is {self.next_task_id}\n"
        )

    @classmethod
    def find_by_id(cls, _id: int):
        """Finds a task with the specified id.
        
        Returns:
            The task with the specified id.
        """

        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        """Adds a task to the database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """Deletes a task from the database."""
        db.session.delete(self)
        db.session.commit()


@unique
class TasksFields(Enum):
    """Represents a task attributes' name.
    
    Attributes:
        ID: Id of a task.
        DESCRIPTION: Description of a task.
        IS_DONE: Boolean specifying the completion of the task.
        COMPLETED_AT: The date on which the task is completed.
        CREATED_AT: The date on which the task was created.
    """

    ID = "id"
    DESCRIPTION = "description"
    IS_DONE = "is_done"
    COMPLETED_AT = "completed_at"
    CREATED_AT = "created_at"

    def values(self):
        """Returns a list containing a task."""
        return list(map(str, self))
