#!/usr/bin/python3.6+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-6-30
@desc: ...
"""
# from typing import Any
# from sqlalchemy.ext.declarative import as_declarative, declared_attr
#
#
# @as_declarative()
# class Base:
#     # Generate __tablename__ automatically
#     @declared_attr
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower()
#
#     id: Any
#     __name__: str

from urllib.parse import splittype
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from yzcore.default_settings import default_setting as settings


def get_db_engine():
    if settings.DB_URI is None:
        raise EnvironmentError('需要配置"DB_URI"变量！')
    _typ, _ = splittype(settings.DB_URI)
    if _typ.startswith('sqlite'):
        return create_engine(
            settings.DB_URI,
            connect_args={"check_same_thread": False}
            # 只有SQLite才需要，其他数据库不需要。SQLite 只允许一个线程与其通信
        )
    else:
        return create_engine(
            settings.DB_URI,
        )


engine = get_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
