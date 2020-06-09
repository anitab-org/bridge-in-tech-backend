import json
from app.database.sqlalchemy_extension import db


class JsonCustomType(db.TypeDecorator):
    """Enables JSON storage by encoding and decoding to Text field."""

    impl = db.Text

    @classmethod
    def process_bind_param(cls, value, dialect):
        if value is None:
            return "{}"
        return json.dumps(value)

    @classmethod
    def process_result_value(cls, value, dialect):
        if value is None:
            return {}
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return None
