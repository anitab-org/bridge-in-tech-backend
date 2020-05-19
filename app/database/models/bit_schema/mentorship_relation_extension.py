from datetime import date

from app.database.models.ms_schema.mentorship_relation import MentorshipRelationModel
from app.database.sqlalchemy_extension import db


class MentorshipRelationExtensionModel(db.Model):
    """Defines attibutes of mentorship relation that are specific only to BridgeInTech.
    
    Attributes:
    program_id: An integer for storing program id.
    mentorship_relation_id: An integer for storing mentorship relation id.
    mentor_agreed_date: A numeric for storing the date when mentor agreed to work in program.
    mentee_agreed_date: A numeric for storing the date when mentee agreed to work in program.
    """

    __tablename__ = "mentorship_relations_extension"
    __table_args__ = {"schema": "bitschema", "extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)

    program_id = db.Column(
        db.Integer,
        db.ForeignKey("bitschema.programs.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    mentorship_relation_id = db.Column(
        db.Integer,
        db.ForeignKey("public.mentorship_relations.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    mentor_request_date = db.Column(db.Numeric("16,6", asdecimal=False))
    mentor_agreed_date = db.Column(db.Numeric("16,6", asdecimal=False))
    mentee_request_date = db.Column(db.Numeric("16,6", asdecimal=False))
    mentee_agreed_date = db.Column(db.Numeric("16,6", asdecimal=False))

    def __init__(self, program_id, mentorship_relation_id):
        self.program_id = program_id
        self.mentorship_relation_id = mentorship_relation_id

        # default values
        self.mentor_request_date = None
        self.mentor_agreed_date = None
        self.mentee_request_date = None
        self.mentee_agreed_date = None

    def json(self):
        """Returns information of mentorship as a json object."""
        return {
            "id": self.id,
            "program_id": self.program_id,
            "mentorship_relation_id": self.mentorship_relation_id,
            "mentor_request_date": self.mentor_request_date,
            "mentor_agreed_date": self.mentor_agreed_date,
            "mentee_request_date": self.mentee_request_date,
            "mentee_agreed_date": self.mentee_agreed_date,
        }

    @classmethod
    def find_by_id(cls, _id) -> "MentorshipRelationExtensionModel":

        """Returns the mentorship_relations_extension that has the passed id.
           Args:
                _id: The id of a mentorship_relations_extension.
        """
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        """Saves the model to the database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """Deletes the record of mentorship relation extension from the database."""
        self.tasks_list.delete_from_db()
        db.session.delete(self)
        db.session.commit()
