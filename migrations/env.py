from __future__ import with_statement

import logging
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

from flask import current_app

config.set_main_option(
    "sqlalchemy.url",
    current_app.config.get("SQLALCHEMY_DATABASE_URI").replace("%", "%%"),
)
import re

schema_names = re.split(r",\s*", "public,bitschema")

target_metadata = current_app.extensions["migrate"].db.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # this callback is used to prevent an auto-migration from being generated
    # when there are no changes to the schema
    # reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, "autogenerate", False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info("No changes in schema detected.")
            else:
                schema_name = context.opts["x_schema_name"]

                upgrade_ops = script.upgrade_ops_list[-1]
                downgrade_ops = script.downgrade_ops_list[-1]

                for op in upgrade_ops.ops + downgrade_ops.ops:
                    op.schema = schema_name
                    if hasattr(op, "ops"):
                        for sub_op in op.ops:
                            sub_op.schema = schema_name

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        for schema_name in ["public", "bitschema"]:
            connection.execute("SET search_path TO %s" % schema_name)
            connection.dialect.default_schema_name = schema_name
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                include_schema=True,
                upgrade_token="%s_upgrades" % schema_name,
                downgrade_token="%s_downgrades" % schema_name,
                process_revision_directives=process_revision_directives,
                **current_app.extensions["migrate"].configure_args,
                x_schema_name=schema_name
            )

        with context.begin_transaction():
            context.run_migrations(schema_name=schema_name)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
