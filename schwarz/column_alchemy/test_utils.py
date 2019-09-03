# -*- coding: utf-8 -*-
# Copyright (c) 2017, 2019 Felix Schwarz
# The source code contained in this file is licensed under the MIT license.
# SPDX-License-Identifier: MIT

from fstrings import f
from pythonic_testcase import *
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker


__all__ = ['DBTestCase']

class DBTestCase(PythonicTestCase):
    def setUp(self):
        super(DBTestCase, self).setUp()
        self.engine = create_engine('sqlite:///:memory:')
        self.connection = self.engine.connect()

    # --- internal helpers ----------------------------------------------------
    def _init_table_with_values(self, columns, insertions=None):
        metadata = MetaData(bind=self.connection)
        table = Table('foo', metadata, *columns)
        metadata.create_all()
        if insertions:
            self._insert_data(table, insertions)
        return table

    def _insert_data(self, table, insertions):
        self.connection.execute(table.insert(), insertions)

    def _fetch_value(self, table):
        "Fetches the DB values via SQLAlchemy (so we should get Enum values)."
        session = self._create_session(self.engine)
        db_value = session.query(table).limit(1).scalar()
        return db_value

    def _fetch_db_value(self, table):
        "Fetches the DB values via low-level SQL."
        select_query = sqlalchemy.text(f('SELECT * FROM {table.name} LIMIT 1'))
        rows = self.connection.execute(select_query)
        row = tuple(rows)[0]
        assert len(row) == 1
        return row[0]

    def _create_session(self, engine):
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return Session()

