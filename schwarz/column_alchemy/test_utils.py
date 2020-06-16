# -*- coding: utf-8 -*-
# Copyright (c) 2017, 2019 Felix Schwarz
# The source code contained in this file is licensed under the MIT license.
# SPDX-License-Identifier: MIT

from fstrings import f
from pythonic_testcase import *
import sqlalchemy
from sqlalchemy import create_engine, Column, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Integer


__all__ = ['DBTestCase']

class DBTestCase(PythonicTestCase):
    def setUp(self):
        super(DBTestCase, self).setUp()
        self.engine = create_engine('sqlite:///:memory:')
        self.connection = self.engine.connect()

    # --- internal helpers ----------------------------------------------------
    def _init_table_with_values(self, columns, insertions=None):
        metadata = MetaData(bind=self.connection)
        if len(columns) == 1:
            id_column = Column('id', Integer(), primary_key=True, autoincrement=True)
            columns = [id_column] + columns
        table = Table('foo', metadata, *columns)
        metadata.create_all()
        if insertions:
            self._insert_data(table, insertions)
        return table

    def _insert_data(self, table, insertions):
        insertion = self.connection.execute(table.insert(), insertions)
        return insertion.inserted_primary_key[0]

    def _fetch_value(self, table, id=None):
        "Fetches the DB values via SQLAlchemy (so we should get Enum values)."
        session = self._create_session(self.engine)
        query = session.query(table)
        if id is not None:
            db_value = query.filter(table.c.id == id).one()
        else:
            db_value = query.one_or_none()
        return db_value[-1] if (db_value is not None) else None

    def _fetch_db_value(self, table):
        "Fetches the DB values via low-level SQL."
        select_query = sqlalchemy.text(f('SELECT * FROM {table.name} LIMIT 1'))
        rows = self.connection.execute(select_query)
        row = tuple(rows)[0]
        assert len(row) == 2
        return row[-1]

    def _create_session(self, engine):
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return Session()

