import time
from sqlalchemy import null
from app.database.sqlalchemy_extension import db
from app.utils.bitschema_utils import OrganizationStatus, Timezone
from app.database.models.bit_schema.program import ProgramModel


class OrganizationModel(db.Model):
    """Defines attributes for the organization.

    Attributes:
        rep_id: A string for storing the organization's rep id.
        name: A string for storing organization's name.
        email: A string for storing organization's email.
        address: A string for storing the organization's address.
        geoloc: A geolocation data using JSON format.
        website: A string for storing the organization's website.
    """

    # Specifying database table used for OrganizationModel
    __tablename__ = "organizations"
    __table_args__ = {"schema": "bitschema", "extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)

    # Organization's representative data
    rep_id = db.Column(db.Integer, db.ForeignKey("public.users.id"), unique=True)
    rep_department = db.Column(db.String(150))

    # Organization data
    name = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(254), nullable=False, unique=True)
    about = db.Column(db.String(500))
    address = db.Column(db.String(254))
    website = db.Column(db.String(150), nullable=False)
    timezone = db.Column(db.Enum(Timezone))
    phone = db.Column(db.String(20))
    status = db.Column(db.Enum(OrganizationStatus))
    join_date = db.Column(db.Numeric("16,6", asdecimal=False))

    # Programs relationship
    programs = db.relationship(
        ProgramModel, backref="organization", cascade="all,delete", passive_deletes=True
    )

    def __init__(self, rep_id, name, email, address, website, timezone):
        """Initialises OrganizationModel class."""
        ## required fields

        self.rep_id = rep_id
        self.name = name
        self.email = email
        self.address = address
        self.website = website
        self.timezone = timezone

        # default values
        self.status = OrganizationStatus.DRAFT
        self.join_date = time.time()

    def json(self):
        """Returns OrganizationModel object in json format."""
        return {
            "id": self.id,
            "rep_id": self.rep_id,
            "rep_department": self.rep_department,
            "name": self.name,
            "email": self.email,
            "about": self.about,
            "address": self.address,
            "website": self.website,
            "timezone": self.timezone,
            "phone": self.phone,
            "status": self.status,
            "join_date": self.join_date,
        }

    def __repr__(self):
        """Returns the organization."""
        return (
            f"Organization's id is {self.id}\n"
            f"Organization's representative is {self.rep_id}\n"
            f"Organization's name is {self.name}.\n"
            f"Organization's email is {self.email}\n"
            f"Organization's address is {self.address}\n"
            f"Organization's website is {self.website}\n"
            f"Organization's timezone is {self.timezone}"
        )

    @classmethod
    def find_by_id(cls, _id) -> "OrganizationModel":

        """Returns the Organization that has the passed id.
           Args:
                _id: The id of an Organization.
        """
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_representative(cls, rep_id: int) -> "OrganizationModel":
        """Returns the organization that has the representative id user searched for. """
        return cls.query.filter_by(rep_id=rep_id).first()

    @classmethod
    def find_by_name(cls, name: str) -> "OrganizationModel":
        """Returns the organization that has the name user searched for. """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_email(cls, email: str) -> "OrganizationModel":
        """Returns the organization that has the email user searched for. """
        return cls.query.filter_by(email=email).first()

    def save_to_db(self) -> None:
        """Adds an organization to the database. """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """Deletes an organization from the database. """
        db.session.delete(self)
        db.session.commit()
