from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base repository class with common CRUD operations."""
    
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get(self, id: Any) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, *, skip: int = 0, limit: int = 100, **filters
    ) -> List[ModelType]:
        query = self.db.query(self.model)
        for field, value in filters.items():
            if hasattr(self.model, field):
                query = query.filter(getattr(self.model, field) == value)
        return query.offset(skip).limit(limit).all()

    def create(self, obj_in: CreateSchemaType, **kwargs) -> ModelType:
        obj_in_data = obj_in.model_dump() if hasattr(obj_in, "model_dump") else obj_in.dict()
        db_obj = self.model(**obj_in_data, **kwargs)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(
        self, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        if hasattr(obj_in, "model_dump"):
            obj_data = obj_in.model_dump(exclude_unset=True)
        elif hasattr(obj_in, 'dict'):
            obj_data = obj_in.dict(exclude_unset=True)
        else:
            obj_data = obj_in
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def remove(self, *, id: int) -> ModelType:
        obj = self.db.get(self.model, id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj

    def get_by_field(self, field: str, value: Any) -> Optional[ModelType]:
        if not hasattr(self.model, field):
            raise ValueError(f"{self.model.__name__} has no attribute {field}")
        return self.db.query(self.model).filter(getattr(self.model, field) == value).first()
