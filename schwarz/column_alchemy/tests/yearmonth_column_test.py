# -*- coding: utf-8 -*-
# Copyright (c) 2017, 2024 Felix Schwarz
# The source code contained in this file is licensed under the MIT license.
# SPDX-License-Identifier: MIT

import pytest
from sqlalchemy import Column

from schwarz.column_alchemy import YearMonth, YearMonthColumn, YearMonthIntColumn


@pytest.mark.parametrize('value', [
    YearMonth(2017, 12),
    YearMonth(1912, 1),
    None,
])
def test_year_month_column_can_store_and_load_values(db_ctx, value):
    value_column = Column('value', YearMonthColumn())
    table = db_ctx.init_table_with_values([value_column])
    with db_ctx.connection.begin():
        inserted_id = db_ctx.insert_data(table, [{'value': value}])

    db_value = db_ctx.fetch_value(table, id=inserted_id)
    assert db_value == value


@pytest.mark.parametrize('value', [
    YearMonth(2017, 12),
    YearMonth(1912, 1),
    None,
])
def test_year_month_int_column_can_store_and_load_values(db_ctx, value):
    value_column = Column('value', YearMonthIntColumn())
    table = db_ctx.init_table_with_values([value_column])
    with db_ctx.connection.begin():
        inserted_id = db_ctx.insert_data(table, [{'value': value}])

    db_value = db_ctx.fetch_value(table, id=inserted_id)
    assert db_value == value

