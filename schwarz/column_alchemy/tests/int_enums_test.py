# -*- coding: utf-8 -*-
# Copyright (c) 2019, 2024 Felix Schwarz
# The source code contained in this file is licensed under the MIT license.
# SPDX-License-Identifier: MIT

from enum import Enum

import pytest
from sqlalchemy import Column
from sqlalchemy.exc import IntegrityError

from .. import IntValuesEnum


def test_int_values_enum_can_store_and_load_int_values(db_ctx):
    NrConsts = Enum('NrConsts', ('ONE', 'TWO'))
    assert NrConsts.ONE.value == 1

    value_column = Column('value', IntValuesEnum(NrConsts))
    table = db_ctx.init_table_with_values([value_column], [{'value': NrConsts.ONE}])
    assert db_ctx.fetch_db_value(table) == 1
    assert db_ctx.fetch_value(table) == NrConsts.ONE

def test_int_values_enum_creates_check_constraint_in_db(db_ctx):
    NrConsts = Enum('NrConsts', ('ONE', 'TWO'))
    assert NrConsts.ONE.value == 1
    value_column = Column('value', IntValuesEnum(NrConsts))
    table = db_ctx.init_table_with_values([value_column])

    with db_ctx.connection.begin():
        db_ctx.insert_data(table, [{'value': NrConsts.TWO}])
        with pytest.raises(IntegrityError):
            db_ctx.insert_data(table, [{'value': 21}])

