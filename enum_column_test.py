# -*- coding: utf-8 -*-
# Copyright (c) 2017 Felix Schwarz
# The source code contained in this file is licensed under the MIT license.

from enum import Enum

from ddt import ddt as DataDrivenTestCase, data
from pythonic_testcase import *
from sqlalchemy import create_engine, Column, MetaData, Table
from sqlalchemy.orm import sessionmaker

from enum_column import ValuesEnum


def create_session(engine):
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return Session()


@DataDrivenTestCase
class ValuesEnumTest(PythonicTestCase):
    def setUp(self):
        super(ValuesEnumTest, self).setUp()
        self.engine = create_engine('sqlite:///:memory:')
        self.connection = self.engine.connect()

    @data('eins', 'zwei', None)
    def test_can_store_and_load_values(self, value):
        class FooEnum(Enum):
            one = 'eins'
            two = 'zwei'
        value2enum = dict((e.value, e) for e in FooEnum.__members__.values())

        value_column = Column('value', ValuesEnum(FooEnum))
        table = self._init_table_with_values([value_column], [{'value': value}])
        session = create_session(self.engine)
        db_value = session.query(table).limit(1).scalar()
        expected_enum = value2enum.get(value)
        assert_equals(expected_enum, db_value)

    def _init_table_with_values(self, columns, insertions=None):
        metadata = MetaData(bind=self.connection)
        table = Table('foo', metadata, *columns)
        metadata.create_all()
        if insertions:
            self._insert_data(table, insertions)
        return table

    def _insert_data(self, table, insertions):
        self.connection.execute(table.insert(), insertions)
