from sqlalchemy.orm import Session
from sqlalchemy import ColumnElement


class GenericORM:

    @classmethod
    def find_all(cls, db: Session):
        return db.query(cls).order_by(cls.id.desc()).all()

    @classmethod
    def create(cls, entity_data, db: Session):
        entity = cls.save(entity_data, db)
        return entity

    @classmethod
    def save(cls, entity, db: Session):
        if entity.id:
            db.merge(entity)
        else:
            db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    @classmethod
    def find_by_id(cls, db: Session, id):
        return db.query(cls).filter(cls.id == id).first()

    @classmethod
    def exists_by_id(cls, db: Session, id):
        return db.query(cls).filter(cls.id == id).first() is not None

    @classmethod
    def delete_by_id(cls, db: Session, id):
        entity = db.query(cls).filter(cls.id == id).first()
        if entity is not None:
            db.delete(entity)
            db.commit()

    @classmethod
    def filter(cls, db: Session, syntax: ColumnElement[bool], order="desc"):
        if order == "desc":
            return db.query(cls).order_by(cls.id.desc()).filter(syntax)
        else:
            return db.query(cls).order_by(cls.id.asc()).filter(syntax)
