# -*- coding: utf-8 -*-
# Copyright (c) 2017, 2019, 2024 Felix Schwarz
# The source code contained in this file is licensed under the MIT license.
# SPDX-License-Identifier: MIT

import pytest
import sqlalchemy
from fstrings import f
from sqlalchemy import create_engine, Column, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Integer


__all__ = [
    'db_ctx',
    'init_table_with_values',
]

class Context(object):
    def __init__(self, engine):
        self.engine = engine
        self.connection = engine.connect()

    def fetch_db_value(self, table):
        return _fetch_db_value(self, table)

    def fetch_value(self, table, id=None):
        return _fetch_value(self, table, id)

    def init_table_with_values(self, columns, insertions=None):
        return init_table_with_values(self, columns, insertions)

    def insert_data(self, table, insertions):
        return _insert_data(self, table, insertions)



@pytest.fixture
def db_ctx():
    engine = create_engine('sqlite:///:memory:')
    return Context(engine)


# --- internal helpers ----------------------------------------------------
def init_table_with_values(ctx, columns, insertions=None):
    metadata = MetaData()
    if len(columns) == 1:
        id_column = Column('id', Integer(), primary_key=True, autoincrement=True)
        columns = [id_column] + columns
    table = Table('foo', metadata, *columns)
    with ctx.connection.begin():
        metadata.create_all(ctx.connection)
        if insertions:
            _insert_data(ctx, table, insertions)
    return table

def _insert_data(ctx, table, insertions):
    insertion = ctx.connection.execute(table.insert(), insertions)
    return insertion.inserted_primary_key[0]

def _fetch_value(ctx, table, id=None):
    "Fetches the DB values via SQLAlchemy (so we should get Enum values)."
    session = _create_session(ctx.engine)
    query = session.query(table)
    if id is not None:
        db_value = query.filter(table.c.id == id).one()
    else:
        db_value = query.one_or_none()
    return db_value[-1] if (db_value is not None) else None

def _fetch_db_value(ctx, table):
    "Fetches the DB values via low-level SQL."
    select_query = sqlalchemy.text(f('SELECT * FROM {table.name} LIMIT 1'))
    rows = ctx.connection.execute(select_query)
    row = tuple(rows)[0]
    assert len(row) == 2
    return row[-1]

def _create_session(engine):
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return Session()

