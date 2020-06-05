"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade(schema_name):
    globals()["upgrade_%s" % schema_name]()


def downgrade(schema_name):
    globals()["downgrade_%s" % schema_name]()

<%
    import re
    schema_names = re.split(r',\s*', "public,bitschema")
%>


% for schema_name in schema_names:

def upgrade_${schema_name}():
    ${context.get("%s_upgrades" % schema_name, "pass")}


def downgrade_${schema_name}():
    ${context.get("%s_downgrades" % schema_name, "pass")}

% endfor 