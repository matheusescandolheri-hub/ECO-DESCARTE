from collections.abc import Generator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


DATABASE_URL = "sqlite:///./eco_descarta.db"


class Base(DeclarativeBase):
    pass


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_db() -> None:
    from app import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    ensure_local_schema()


def ensure_local_schema() -> None:
    inspector = inspect(engine)
    if not inspector.has_table("pontos_coleta"):
        return

    existing_columns = {
        column["name"] for column in inspector.get_columns("pontos_coleta")
    }
    columns_to_add = {
        "telefone": "VARCHAR(40)",
        "horario_funcionamento": "VARCHAR(160)",
        "observacao": "TEXT",
        "fonte_dados": "VARCHAR(180)",
        "ativo": "BOOLEAN NOT NULL DEFAULT 1",
    }

    with engine.begin() as connection:
        for column_name, column_type in columns_to_add.items():
            if column_name not in existing_columns:
                connection.execute(
                    text(f"ALTER TABLE pontos_coleta ADD COLUMN {column_name} {column_type}")
                )


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
