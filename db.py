from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base


def get_session(db_path: str):
    """Provides a connection to the database through sqlalchemy session"""
    engine= create_engine(f"sqlite:///{db_path}", echo=True)
    S = sessionmaker(engine, expire_on_commit=True)
    return S()

def initialize_db_tool(db_path: str) -> None:
    globalbase = Base
    engine= create_engine(f"sqlite:///{db_path}", echo=False)
    globalbase.metadata.bind = engine
    globalbase.metadata.drop_all()
    globalbase.metadata.create_all()