# -*- coding: utf-8 -*-
# Copyright (c) 2017 Felix Schwarz
# The source code contained in this file is licensed under the MIT license.
# SPDX-License-Identifier: MIT

from __future__ import absolute_import, print_function, unicode_literals

from decimal import Decimal

from ddt import ddt as DataDrivenTestCase, data
from pythonic_testcase import *
from sqlalchemy import Column
from sqlalchemy.exc import StatementError

from .. import ShiftedDecimal
from ..test_utils import DBTestCase


@DataDrivenTestCase
class ShiftedDecimalTest(DBTestCase):
    @data(Decimal('987.1234'), 4711, None)
    def test_can_store_and_load_values(self, value):
        c_value = Column('value', ShiftedDecimal(4))
        table = self._init_table_with_values([c_value])
        inserted_id = self._insert_data(table, [{'value': value}])

        db_value = self._fetch_value(table, id=inserted_id)
        assert_equals(value, db_value)

    def test_refuse_to_store_more_decimal_places(self):
        bad_value = Decimal('98.123')
        c_value = Column('value', ShiftedDecimal(2))
        table = self._init_table_with_values([c_value])
        with assert_raises(StatementError):
            self._insert_data(table, [{'value': bad_value}])

        db_value = self._fetch_value(table)
        assert_none(db_value)


