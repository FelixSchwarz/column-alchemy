# -*- coding: utf-8 -*-
# Copyright (c) 2017, 2024 Felix Schwarz
# The source code contained in this file is licensed under the MIT license.
# SPDX-License-Identifier: MIT

from decimal import Decimal

import pytest
from sqlalchemy import Column
from sqlalchemy.exc import StatementError

from schwarz.column_alchemy import ShiftedDecimal


@pytest.mark.parametrize('value', [
    Decimal('987.1234'),
    4711,
    None,
])
def test_shifted_decimal_can_store_and_load_values(db_ctx, value):
    c_value = Column('value', ShiftedDecimal(4))
    table = db_ctx.init_table_with_values([c_value])
    with db_ctx.connection.begin():
        inserted_id = db_ctx.insert_data(table, [{'value': value}])

    db_value = db_ctx.fetch_value(table, id=inserted_id)
    assert db_value == value


def test_shifted_decimal_refuses_to_store_more_decimal_places(db_ctx):
    bad_value = Decimal('98.123')
    c_value = Column('value', ShiftedDecimal(2))
    table = db_ctx.init_table_with_values([c_value])
    with pytest.raises(StatementError):
        db_ctx.insert_data(table, [{'value': bad_value}])

    db_value = db_ctx.fetch_value(table)
    assert db_value is None
