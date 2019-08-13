# -*- coding: utf-8 -*-
# Copyright 2013, 2018 Felix Schwarz
# The source code in this file is dual licensed under the MIT license or
# the GPLv3 or (at your option) any later version.
# SPDX-License-Identifier: MIT or GPL-3.0-or-later

from __future__ import absolute_import

from datetime import datetime as DateTime

from babel.util import FixedOffsetTimezone, UTC
from pythonic_testcase import *
from sqlalchemy import Column, Integer, MetaData, Table
from sqlalchemy.engine import create_engine
from sqlalchemy.sql import select

from ..utc_datetime_column import UTCDateTime


class UTCDateTimeTest(PythonicTestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.metadata = MetaData(bind=self.engine)
        self.table = Table('utc_datetime', self.metadata,
            Column('id', Integer(), primary_key=True, autoincrement=True),
            Column('timestamp', UTCDateTime)
        )
        self.metadata.create_all()
        self.db = self.engine.connect()

    def tearDown(self):
        self.metadata.drop_all()

    def _insert(self, dt):
        insertion = self.db.execute(
            self.table.insert().values(timestamp=dt)
        )
        return insertion.inserted_primary_key[0]

    def _fetch(self, item_id):
        result = self.db.execute(
            select([self.table]).where(self.table.c.id == item_id)
        ).fetchone()
        return result

    def test_can_store_datetime_with_timezone(self):
        dt = DateTime(2013, 5, 25, 9, 53, 24, tzinfo=FixedOffsetTimezone(-90))
        inserted_id = self._insert(dt)

        result = self._fetch(inserted_id)
        assert_equals(1, result[0])
        dt_from_db = result[1]
        assert_equals(dt, dt_from_db)
        assert_equals(UTC, dt_from_db.tzinfo)

    def test_raises_exception_for_naive_datetime(self):
        dt = DateTime(2013, 5, 25, 9, 53, 24)
        with assert_raises(ValueError):
            self._insert(dt)

    def test_can_store_none(self):
        inserted_id = self._insert(None)
        result = self._fetch(inserted_id)
        assert_equals((1, None), result)

