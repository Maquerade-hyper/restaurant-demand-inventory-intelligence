from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from .config import get_settings


def create_db_engine() -> Engine:
    settings = get_settings()
    return create_engine(
        settings.sqlalchemy_database_url,
        pool_pre_ping=True,
        future=True,
    )


def check_database_connection(engine: Engine | None = None) -> dict:
    engine = engine or create_db_engine()
    with engine.connect() as connection:
        version = connection.execute(text("SELECT version()" )).scalar_one()
    return {"status": "ok", "version": version}
