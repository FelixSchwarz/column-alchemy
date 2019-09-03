# -*- coding: utf-8 -*-
# Copyright (c) 2017, 2019 Felix Schwarz
# The source code contained in this file is licensed under the MIT license.
# SPDX-License-Identifier: MIT

from enum import Enum

from ddt import ddt as DataDrivenTestCase, data
from pythonic_testcase import *
from sqlalchemy import Column

from .. import ValuesEnum
from ..test_utils import DBTestCase


@DataDrivenTestCase
class ValuesEnumTest(DBTestCase):
    @data('eins', 'zwei', None)
    def test_can_store_and_load_values(self, value):
        class FooEnum(Enum):
            one = 'eins'
            two = 'zwei'
        value2enum = dict((e.value, e) for e in FooEnum.__members__.values())

        value_column = Column('value', ValuesEnum(FooEnum))
        table = self._init_table_with_values([value_column], [{'value': value}])
        expected_enum = value2enum.get(value)
        assert_equals(expected_enum, self._fetch_value(table))
        assert_equals(value, self._fetch_db_value(table))

    def test_can_store_and_load_int_values(self):
        NrConsts = Enum('NrConsts', ('ONE', 'TWO'))
        assert_equals(1, NrConsts.ONE.value)

        value_column = Column('value', ValuesEnum(NrConsts))
        table = self._init_table_with_values([value_column], [{'value': NrConsts.ONE}])
        assert_equals('1', self._fetch_db_value(table),)
        assert_equals(NrConsts.ONE, self._fetch_value(table))

