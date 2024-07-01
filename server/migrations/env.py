import logging
from logging.config import fileConfig

from flask import current_app
from alembic import context

# Alembic Config object to access the values within the .ini file in use.
config = context.config

# Set up logging configuration from the config file.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

def retrieve_engine():
    try:
        # Compatibility with Flask-SQLAlchemy<3 and Alchemical
        return current_app.extensions['migrate'].db.get_engine()
    except TypeError:
        # Compatibility with Flask-SQLAlchemy>=3
        return current_app.extensions['migrate'].db.engine

def retrieve_engine_url():
    try:
        return retrieve_engine().url.render_as_string(hide_password=False).replace('%', '%%')
    except AttributeError:
        return str(retrieve_engine().url).replace('%', '%%')

# Setting the SQLAlchemy URL for Alembic.
config.set_main_option('sqlalchemy.url', retrieve_engine_url())
target_db = current_app.extensions['migrate'].db

def fetch_metadata():
    if hasattr(target_db, 'metadatas'):
        return target_db.metadatas[None]
    return target_db.metadata

def perform_offline_migrations():
    """Execute migrations in 'offline' mode.

    Configures the context with a URL without creating an Engine.
    This avoids the need for a DBAPI to be available.

    Calls to context.execute() here emit the given string to the script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=fetch_metadata(), literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def perform_online_migrations():
    """Execute migrations in 'online' mode.

    Creates an Engine and associates a connection with the context.
    """

    def filter_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No schema changes detected.')

    connectable = retrieve_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=fetch_metadata(),
            process_revision_directives=filter_revision_directives,
            **current_app.extensions['migrate'].configure_args
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    perform_offline_migrations()
else:
    perform_online_migrations()
