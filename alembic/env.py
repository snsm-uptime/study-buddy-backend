import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from app.config import get_settings
from app.db.base import Base
from app.db.models import file, file_chunk

# ---------------------
# Alembic Config Setup
# ---------------------
config = context.config
settings = get_settings()

# Inject DB URL from your app settings
config.set_main_option("sqlalchemy.url", settings.database_url)

# Interpret the config file for Python logging
fileConfig(config.config_file_name)

# Target metadata for autogeneration
target_metadata = Base.metadata


# ----------------------------
# Offline Migration Execution
# ----------------------------
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ----------------------------
# Online Migration Execution
# ----------------------------
async def run_migrations_online():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    async with connectable.connect() as connection:

        def do_run_migrations(connection):
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                compare_type=True,
            )
            with context.begin_transaction():
                context.run_migrations()

        await connection.run_sync(do_run_migrations)


# Entrypoint
def run():
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())


run()
