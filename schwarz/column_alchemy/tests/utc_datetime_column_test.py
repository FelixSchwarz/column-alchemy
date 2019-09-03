# -*- coding: utf-8 -*-
# Copyright 2013, 2018, 2019 Felix Schwarz
# The source code in this file is dual licensed under the MIT license or
# the GPLv3 or (at your option) any later version.
# SPDX-License-Identifier: MIT or GPL-3.0-or-later

from __future__ import absolute_import

from datetime import datetime as DateTime

from babel.util import FixedOffsetTimezone, UTC
from pythonic_testcase import *
from sqlalchemy import Column
from sqlalchemy.exc import StatementError

from .. import UTCDateTime
from ..test_utils import DBTestCase


class UTCDateTimeTest(DBTestCase):
    def setUp(self):
        super(UTCDateTimeTest, self).setUp()
        ts_column = Column('timestamp', UTCDateTime)
        self.table = self._init_table_with_values([ts_column])

    def test_can_store_datetime_with_timezone(self):
        dt = DateTime(2013, 5, 25, 9, 53, 24, tzinfo=FixedOffsetTimezone(-90))
        inserted_id = self._insert_data(self.table, [{'timestamp': dt}])

        dt_from_db = self._fetch_value(self.table, id=inserted_id)
        assert_equals(dt, dt_from_db)
        assert_equals(UTC, dt_from_db.tzinfo)

    def test_raises_exception_for_naive_datetime(self):
        dt = DateTime(2013, 5, 25, 9, 53, 24)
        with assert_raises(StatementError):
            self._insert_data(self.table, [{'timestamp': dt}])

    def test_can_store_none(self):
        inserted_id = self._insert_data(self.table, [{'timestamp': None}])
        assert_none(self._fetch_value(self.table))

