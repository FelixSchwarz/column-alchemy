# -*- coding: utf-8 -*-
# Copyright (c) 2017 Felix Schwarz
# The source code contained in this file is licensed under the MIT license.
# SPDX-License-Identifier: MIT

from __future__ import absolute_import, print_function, unicode_literals

from ddt import ddt as DataDrivenTestCase, data as ddt_data
from pythonic_testcase import *
from sqlalchemy import Column

from ..test_utils import DBTestCase
from ..yearmonth_column import YearMonth, YearMonthColumn, YearMonthIntColumn


@DataDrivenTestCase
class YearMonthColumnTest(DBTestCase):
    @ddt_data(YearMonth(2017, 12), YearMonth(1912, 1), None)
    def test_can_store_and_load_values(self, value):
        value_column = Column('value', YearMonthColumn())
        table = self._init_table_with_values([value_column])
        inserted_id = self._insert_data(table, [{'value': value}])

        db_value = self._fetch_value(table, id=inserted_id)
        assert_equals(value, db_value)


@DataDrivenTestCase
class YearMonthIntColumnTest(DBTestCase):
    @ddt_data(YearMonth(2017, 12), YearMonth(1912, 1), None)
    def test_can_store_and_load_values(self, value):
        value_column = Column('value', YearMonthIntColumn())
        table = self._init_table_with_values([value_column])
        inserted_id = self._insert_data(table, [{'value': value}])

        db_value = self._fetch_value(table, id=inserted_id)
        assert_equals(value, db_value)

