from sqlalchemy import null
from sqlalchemy.dialects.postgresql import JSONB
from app.database.sqlalchemy_extension import db
from app.utils.bitschema_utils import Timezone


class UserExtensionModel(db.Model):
    """Defines attributes for a user that are specific only to BridgeInTech.
    Attributes:
    user_id: A string for storing user_id.
    is_organization_rep: A boolean indicating that user is a organization representative.
    additional_info: A json object for storing other information of the user with the specified id.
    timezone: A string for storing user timezone information.
    """

    # Specifying database table used for UserExtensionModel
    __tablename__ = "users_extension"
    __table_args__ = {"schema": "bitschema", "extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("public.users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    is_organization_rep = db.Column(db.Boolean)
    additional_info = db.Column(JSONB(none_as_null=False), default=JSONB.NULL)
    timezone = db.Column(db.Enum(Timezone))

    """Initialises UserExtensionModel class."""
    ## required fields
    def __init__(self, user_id, timezone):
        self.user_id = user_id
        self.timezone = timezone

        # default value
        self.is_organization_rep = False
        self.additional_info = None

    def json(self):
        """Returns UserExtensionmodel object in json format."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "is_organization_rep": self.is_organization_rep,
            "timezone": self.timezone,
            "additional_info": self.additional_info,
        }

    def __repr__(self):
        """Returns user's information that is specific to BridgeInTech."""

        return (
            f"Users's id is {self.user_id}.\n"
            f"User's as organization representative is: {self.is_organization_rep}\n"
            f"User's timezone is: {self.timezone}\n"
        )

    @classmethod
    def find_by_user_id(cls, user_id) -> "UserExtensionModel":

        """Returns the user extension that has the passed user id.
           Args:
                _id: The id of a user.
        """
        return cls.query.filter_by(user_id=user_id).first()

    def save_to_db(self) -> None:
        """Adds user's BridgeInTech specific data to the database. """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """Deletes user's BridgeInTech specific data from the database. """
        db.session.delete(self)
        db.session.commit()
