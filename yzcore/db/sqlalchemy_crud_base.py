#!/usr/bin/python3.6+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-6-30
@desc: ...
"""
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

try:
    from pydantic import BaseModel
    import sqlalchemy
    from sqlalchemy import text
    from sqlalchemy.orm import Session
    from sqlalchemy.ext.declarative import as_declarative, declared_attr
except ImportError:
    pass

from yzcore.core.encoders import jsonable_encoder


@as_declarative()
class Base:
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Any
    __name__: str


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class OrmCRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        assert sqlalchemy is not None, "'sqlalchemy' must be installed to use OrmCRUDBase"
        self.model = model

    def count(self, db: Session, **kwargs):
        """
        根据条件获取总数量

        :param db:
        :param kwargs:
        :return:
        """
        if kwargs:
            return db.query(self.model).filter_by(**kwargs).count()
        return db.query(self.model).count()

    def get(self, db: Session, model_id: Any) -> Optional[ModelType]:
        """
        根据id获取数据

        :param db:
        :param model_id:
        :return:
        """
        return db.query(self.model).get(model_id)
    
    def get_one(self, db: Session, **kwargs):
        """
        根据查询条件获取一个数据
        
        :param db: 
        :param kwargs: 
        :return: 
        """
        return db.query(self.model).filter_by(**kwargs).one_or_none()
    
    def list(
            self, db: Session, *, sort: List[str] = None, offset: int = 0,
            limit: int = 100, **kwargs
    ) -> List[ModelType]:
        """
        根据查询条件获取数据列表

        :param db:
        :param sort: 需要排序的字段 ['-create_time', 'update_time'] (负号为降序)
        :param offset:
        :param limit:
        :param kwargs:
        :return:
        """
        if sort:
            sort = [text(s) for s in sort]
        if kwargs:
            return db.query(self.model).filter_by(
                **kwargs).order_by(sort).offset(offset).limit(limit).all()
        else:
            return db.query(self.model).order_by(sort).offset(
                offset).limit(limit).all()

    def create(
            self, db: Session, *,
            data: Union[Dict[str, Any], CreateSchemaType],
            is_transaction: bool = False
    ) -> ModelType:
        """
        插入操作，返回创建的模型

        :param db:
        :param data: 创建所需的数据
        :param is_transaction: 是否开启事务功能
        :return:
        """
        if isinstance(data, BaseModel):
            data = jsonable_encoder(data)
        db_obj = self.model(**data)  # type: ignore
        db.add(db_obj)
        if not is_transaction:
            db.commit()
            db.refresh(db_obj)
        return db_obj

    def update(
            self,
            db: Session, *,
            model_id: int = None,
            obj: ModelType = None,
            query: Dict[str, Any] = None,
            data: Union[UpdateSchemaType, Dict[str, Any]],
            is_return_obj: bool = False,
            is_transaction: bool = False

    ) -> ModelType:
        """
        单个对象更新

        更新有两种方式：
        方式一：
                传入需要更新的模型和更新的数据。
        方式二：
                传入id和更新的数据
        注意：
            如果传入模型来进行更新，则'is_return_obj=False'失效，返回更新后的模型

        :param db:
        :param model_id:    模型ID
        :param obj:         模型对象
        :param query:       模型查询参数
        :param data:        需要更新的数据
        :param is_return_obj:   是否需要返回模型数据，默认为False，只返回更新成功的行数
        :param is_transaction:  是否开启事务功能

        :return: update_count or obj or None
        """
        if not any((model_id, obj, query)):
            raise ValueError('At least one of [model_id、query、obj] exists')

        if isinstance(data, dict):
            update_data = data
        else:
            update_data = data.dict(exclude_unset=True)

        if not is_return_obj and not obj:
            if model_id:
                update_count = db.query(self.model).filter(
                    self.model.id == model_id).update(update_data)
            else:
                update_count = db.query(self.model).filter_by(
                    **query).update(update_data)

            if not is_transaction:
                db.commit()
            return update_count
        else:
            if not obj:
                if model_id:
                    obj = self.get(db, model_id)
                else:
                    obj = self.get_one(db, **query)
            if obj:
                obj_data = jsonable_encoder(obj)

                for field in obj_data:
                    if field in update_data:
                        setattr(obj, field, update_data[field])
                db.add(obj)
                if not is_transaction:
                    db.commit()
                db.refresh(obj)
                return obj

    def delete(
            self, db: Session, *,
            model_id: int,
            is_return_obj: bool = False,
            is_transaction: bool = False
    ) -> ModelType:
        """

        :param db:
        :param model_id:      模型ID
        :param is_return_obj: 是否需要返回模型数据，默认为False，只返回删除成功的行数
        :param is_transaction:  是否开启事务功能
        :return:
        """
        if is_return_obj:
            obj = db.query(self.model).get(model_id)
            db.delete(obj)
            if not is_transaction:
                db.commit()
            return obj
        else:
            del_count = db.query(self.model).filter(
                self.model.id == model_id).delete(synchronize_session=False)
            if not is_transaction:
                db.commit()
            return del_count

    def bulk_delete(self, db: Session, ids: List[int] = None, **kwargs):
        """

        :param db:
        :param kwargs:
        :return:
        """
        if ids:
            del_count = db.query(self.model).filter(
                self.model.id.in_(ids)).delete(synchronize_session=False)
        else:
            del_count = db.query(self.model).filter_by(
                **kwargs).delete(synchronize_session=False)
        return del_count
