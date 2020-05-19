import re
from app.database.sqlalchemy_extension import db


class ArrayOfEnum(db.TypeDecorator):

    impl = db.ARRAY

    def bind_expression(self, bindvalue):
        return db.cast(bindvalue, self)

    def result_processor(self, dialect, coltype):
        super_rp = super(ArrayOfEnum, self).result_processor(dialect, coltype)

        def handle_raw_string(value):
            inner = re.match(r"^{(.*)}$", value).group(1)
            return inner.split(",")

        def process(value):
            return super_rp(handle_raw_string(value))

        return process
