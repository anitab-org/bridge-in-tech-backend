from datetime import date

from app.database.models.ms_schema.tasks_list import TasksListModel
# from app.database.models.bitschema import MentorshipRelationExtensionModel
from app.database.sqlalchemy_extension import db
from app.utils.enum_utils import MentorshipRelationState


class MentorshipRelationModel(db.Model):
    """Data Model representation of a mentorship relation.
    
    Attributes:
        mentor_id: integer indicates the id of the mentor.
        mentee_id: integer indicates the id of the mentee.
        action_user_id: integer indicates id of action user.
        mentor: relationship between UserModel and mentorship_relation.
        mentee: relationship between UserModel and mentorship_relation.
        creation_date: numeric that defines the date of creation of the mentorship.
        accept_date: numeric that indicates the date of acceptance of mentorship without a program.
        start_date: numeric that indicates the starting date of mentorship which also starts of the program (if any).
        end_date: numeric that indicates the ending date of mentorship which also ends of the program (if any).
        state: enumeration that indicates state of mentorship.
        notes: string that indicates any notes.
        tasks_list_id: integer indicates the id of the tasks_list
        tasks_list: relationship between TasksListModel and mentorship_relation.
        mentor_agreed: numeric that indicates the date when mentor accepted to a program.
        mentee_agreed: numeric that indicates the date when mentee accepted to a program.
    """

    # Specifying database table used for MentorshipRelationModel
    __tablename__ = "mentorship_relations"
    __table_args__ = {"schema": "public", "extend_existing": True}
    
    id = db.Column(db.Integer, primary_key=True)

    
    # personal data
    mentor_id = db.Column(db.Integer, db.ForeignKey("public.users.id"))
    mentee_id = db.Column(db.Integer, db.ForeignKey("public.users.id"))
    action_user_id = db.Column(db.Integer, nullable=False)
    mentor = db.relationship(
        # UserModel,
        "UserModel",
        backref="mentor_relations",
        primaryjoin="MentorshipRelationModel.mentor_id == UserModel.id",
    )
    mentee = db.relationship(
        # UserModel,
        "UserModel",
        backref="mentee_relations",
        primaryjoin="MentorshipRelationModel.mentee_id == UserModel.id",
    )

    creation_date = db.Column(db.Numeric("16,6", asdecimal=False), nullable=False)
    
    accept_date = db.Column(db.Numeric("16,6", asdecimal=False))
    
    start_date = db.Column(db.Numeric("16,6", asdecimal=False)) 
    end_date = db.Column(db.Numeric("16,6", asdecimal=False)) 

    state = db.Column(db.Enum(MentorshipRelationState), nullable=False)
    notes = db.Column(db.String(400))

    tasks_list_id = db.Column(db.Integer, db.ForeignKey("public.tasks_list.id"))
    tasks_list = db.relationship(
        TasksListModel, uselist=False, backref="mentorship_relation"
    )

    mentorship_relation_extension = db.relationship(
        "MentorshipRelationExtensionModel",
        backref="mentorship_relation",
        uselist=False,
        cascade="all,delete",
        passive_deletes=True,
    )
    

    # pass in parameters in a dictionary
    def __init__(
        self,
        action_user_id,
        mentor_user,
        mentee_user,
        creation_date,
        end_date,
        state,
        notes,
        tasks_list,
    ):

        self.action_user_id = action_user_id
        self.mentor = mentor_user
        self.mentee = mentee_user  # same as mentee_user.mentee_relations.append(self)
        self.creation_date = creation_date
        self.end_date = end_date
        self.state = state
        self.notes = notes
        self.tasks_list = tasks_list

    def json(self):
        """Returns information of mentorship as a json object."""
        return {
            "id": self.id,
            "action_user_id": self.action_user_id,
            "mentor_id": self.mentor_id,
            "mentee_id": self.mentee_id,
            "creation_date": self.creation_date,
            "accept_date": self.accept_date,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "state": self.state,
            "notes": self.notes,
        }

    
    @classmethod
    def find_by_id(cls, _id) -> "MentorshipRelationModel":

        """Returns the mentorship that has the passed id.
           Args:
                _id: The id of a mentorship.
        """
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def is_empty(cls) -> bool:
        """Returns True if the mentorship model is empty, and False otherwise."""
        return cls.query.first() is None

    @classmethod
    def find_by_program_id(cls, program_id):

        """Returns list of mentorship that has the passed program id.
           Args:
                program_id: The id of a program which the mentorships related to.
        """
        return cls.query.filter_by(program_id=program_id).first().all

    def save_to_db(self) -> None:
        """Saves the model to the database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """Deletes the record of mentorship relation from the database."""
        self.tasks_list.delete_from_db()
        db.session.delete(self)
        db.session.commit()
