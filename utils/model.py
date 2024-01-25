from database import Base, db_dependency
from fastapi import HTTPException


def get_all(
    model: Base,
    db: db_dependency,
):
    return db.query(model).all()


def get_model_by_id(
    model: Base,
    id: int,
    db: db_dependency,
):
    return db.query(model).filter(model.id == id).first()


def delete_model_by_id(model: Base, id: int, db: db_dependency):
    model = get_model_by_id(model, id, db)
    if model is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    db.delete(model)
    db.commit()
