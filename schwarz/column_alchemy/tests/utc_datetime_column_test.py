# -*- coding: utf-8 -*-
# Copyright 2013, 2018, 2019, 2024 Felix Schwarz
# The source code in this file is dual licensed under the MIT license or
# the GPLv3 or (at your option) any later version.
# SPDX-License-Identifier: MIT or GPL-3.0-or-later

from datetime import datetime as DateTime, timedelta as TimeDelta, timezone

import pytest
from sqlalchemy import Column
from sqlalchemy.exc import StatementError

from .. import UTCDateTime


@pytest.fixture
def ctx(db_ctx):
    ts_column = Column('timestamp', UTCDateTime)
    table = db_ctx.init_table_with_values([ts_column])
    db_ctx.table = table
    return db_ctx


def test_utc_datetime_can_store_datetime_with_timezone(ctx):
    tz = timezone(TimeDelta(hours=-1, minutes=-30))
    dt = DateTime(2013, 5, 25, 9, 53, 24, tzinfo=tz)
    with ctx.connection.begin():
        inserted_id = ctx.insert_data(ctx.table, [{'timestamp': dt}])

    dt_from_db = ctx.fetch_value(ctx.table, id=inserted_id)
    assert dt_from_db == dt
    assert dt_from_db.tzinfo == timezone.utc


def test_utc_datetime_raises_exception_for_naive_datetime(ctx):
    dt = DateTime(2013, 5, 25, 9, 53, 24)
    with pytest.raises(StatementError):
        ctx.insert_data(ctx.table, [{'timestamp': dt}])


def test_utc_datetime_can_store_none(ctx):
    with ctx.connection.begin():
        _inserted_id = ctx.insert_data(ctx.table, [{'timestamp': None}])
    assert ctx.fetch_value(ctx.table) is None
