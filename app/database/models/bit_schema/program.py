import time
from sqlalchemy import null
from sqlalchemy import BigInteger, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from app.database.sqlalchemy_extension import db
from app.utils.bitschema_utils import ContactType, Zone, ProgramStatus
# from app.database.models.ms_schema.mentorship_relation import MentorshipRelationModel
from app.database.models.bit_schema.mentorship_relation_extension import (
    MentorshipRelationExtensionModel,
)


class ProgramModel(db.Model):
    """Defines attributes for a program.

    Attributes:
    program_name: A string for storing program name.
    organization_id: An integer for storing organization's id.
    start_date: A date for storing the program start date.
    end_date: A date for storing the program end date. 
    """

    # Specifying database table used for ProgramModel
    __tablename__ = "programs"
    __table_args__ = {"schema": "bitschema", "extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)

    program_name = db.Column(db.String(100), unique=True, nullable=False)
    organization_id = db.Column(
        db.Integer,
        db.ForeignKey("bitschema.organizations.id", ondelete="CASCADE"),
        nullable=False,
    )
    start_date = db.Column(db.Numeric("16,6", asdecimal=False))
    end_date = db.Column(db.Numeric("16,6", asdecimal=False))
    description = db.Column(db.String(500))
    target_skills = db.Column(ARRAY(db.String(150)))
    target_candidate = db.Column(JSONB(none_as_null=False), default=JSONB.NULL)
    payment_currency = db.Column(db.String(3))
    payment_amount = db.Column(BigInteger)
    contact_type = db.Column(db.Enum(ContactType))
    zone = db.Column(db.Enum(Zone))
    student_responsibility = db.Column(ARRAY(db.String(250)))
    mentor_responsibility = db.Column(ARRAY(db.String(250)))
    organization_responsibility = db.Column(ARRAY(db.String(250)))
    student_requirements = db.Column(ARRAY(db.String(250)))
    mentor_requirements = db.Column(ARRAY(db.String(250)))
    resources_provided = db.Column(ARRAY(db.String(250)))
    contact_name = db.Column(db.String(50))
    contact_department = db.Column(db.String(150))
    program_address = db.Column(db.String(250))
    contact_phone = db.Column(db.String(20))
    contact_mobile = db.Column(db.String(20))
    contact_email = db.Column(db.String(254))
    program_website = db.Column(db.String(254))
    irc_channel = db.Column(db.String(254))
    tags = db.Column(ARRAY(db.String(150)))
    status = db.Column(db.Enum(ProgramStatus))
    creation_date = db.Column(db.Numeric("16,6", asdecimal=False))
    mentorship_relation = db.relationship(
        MentorshipRelationExtensionModel,
        backref="program",
        uselist=False,
        cascade="all,delete",
        passive_deletes=True,
    )

    """Initialises ProgramModel class."""
    ## required fields
    def __init__(self, program_name, organization_id, start_date, end_date):
        self.program_name = program_name
        self.organization = organization_id
        self.start_date = start_date
        self.end_date = end_date

        # default value
        self.target_candidate = None
        self.status = ProgramStatus.DRAFT
        self.creation_date = time.time()

    def json(self):
        """Returns ProgramModel object in json format."""
        return {
            "id": self.id,
            "program_name": self.program_name,
            "organization_id": self.organization_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "target_skills": self.target_skills,
            "target_candidate": self.target_candidate,
            "payment_currency": self.payment_currency,
            "payment_amount": self.payment_amount,
            "contact_type": self.contact_type,
            "zone": self.zone,
            "student_responsibility": self.student_responsibility,
            "mentor_responsibility": self.mentor_responsibility,
            "organization_responsibility": self.organization_responsibility,
            "student_requirements": self.student_requirements,
            "mentor_requirements": self.mentor_requirements,
            "resources_provided": self.resources_provided,
            "contact_name": self.contact_name,
            "contact_department": self.contact_department,
            "program_address": self.program_address,
            "contact_phone": self.contact_phone,
            "contact_mobile": self.contact_mobile,
            "contact_email": self.contact_email,
            "program_website": self.program_website,
            "irc_channel": self.irc_channel,
            "tags": self.tags,
            "status": self.status,
            "creation_date": self.creation_date,
        }

    def __repr__(self):
        """Returns the program name, creation/start/end date and organization id."""
        return (
            f"Program id is {self.program.id}\n"
            f"Program name is {self.program_name}.\n"
            f"Organization's id is {self.organization_id}.\n"
            f"Program start date is {self.start_date}\n"
            f"Program end date is {self.end_date}\n"
            f"Program creation date is {self.creation_date}\n"
        )

    @classmethod
    def find_by_id(cls, _id) -> "ProgramModel":

        """Returns the Program that has the passed id.
           Args:
                _id: The id of a Program.
        """
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, program_name) -> "ProgramModel":

        """Returns the Program that has the passed name.
           Args:
                program_name: The name of a Program.
        """
        return cls.query.filter_by(program_name=program_name).first()
    
    @classmethod
    def get_all_programs_by_organization(cls, organization_id):
        """Returns list of programs that has the passed organization id.
           Args:
                _id: The id of an Organization.
        """
        return cls.query.filter_by(organization_id=organization_id).all()
    
    @classmethod
    def get_all_programs_by_representative(cls, rep_id):
        """Returns list of programs that where their representative ID is the passedid."""
        return cls.query.filter_by(rep_id=rep_id).all()

    def save_to_db(self) -> None:
        """Adds a program to the database. """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """Deletes a program from the database. """
        db.session.delete(self)
        db.session.commit()
