# -*- coding: utf-8 -*-
# Copyright (c) 2019 Felix Schwarz
# The source code contained in this file is licensed under the MIT license.
# SPDX-License-Identifier: MIT

from enum import Enum

from pythonic_testcase import *
from sqlalchemy import Column
from sqlalchemy.exc import IntegrityError, StatementError

from .. import IntValuesEnum
from ..test_utils import DBTestCase


class IntValuesEnumTest(DBTestCase):
    def test_can_store_and_load_int_values(self):
        NrConsts = Enum('NrConsts', ('ONE', 'TWO'))
        assert_equals(1, NrConsts.ONE.value)

        value_column = Column('value', IntValuesEnum(NrConsts))
        table = self._init_table_with_values([value_column], [{'value': NrConsts.ONE}])
        assert_equals(1, self._fetch_db_value(table),)
        assert_equals(NrConsts.ONE, self._fetch_value(table))

    def test_creates_check_constraint_in_db(self):
        NrConsts = Enum('NrConsts', ('ONE', 'TWO'))
        assert_equals(1, NrConsts.ONE.value)
        value_column = Column('value', IntValuesEnum(NrConsts))
        table = self._init_table_with_values([value_column])

        self._insert_data(table, [{'value': NrConsts.TWO}])
        with assert_raises(IntegrityError):
            self._insert_data(table, [{'value': 21}])

