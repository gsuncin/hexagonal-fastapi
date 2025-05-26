from src.adapters.driven.database.base import SessionLocal


def generate_db():
    return SessionLocal()
