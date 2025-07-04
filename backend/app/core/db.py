# app/core/db.py
from sqlmodel import Session, create_engine, select  # type: ignore

from app import crud
from app.core.config import settings
from app.models import User, UserCreate

# Se crea el motor de conexión a la base de datos usando la URL generada a partir de settings
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def get_session() -> Session:
    """Crea y retorna una sesión de la base de datos."""
    with Session(engine) as session:
        yield session


# Alias for backward compatibility
get_db = get_session

# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)
