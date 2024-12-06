# -*- coding: utf-8 -*-
# Copyright (c) 2017, 2019, 2024 Felix Schwarz
# The source code contained in this file is licensed under the MIT license.
# SPDX-License-Identifier: MIT

from enum import Enum

import pytest
from sqlalchemy import Column

from .. import ValuesEnum


@pytest.mark.parametrize('value', [
    'eins',
    'zwei',
    None,
])
def test_values_enum_can_store_and_load_values(db_ctx, value):
    class FooEnum(Enum):
        one = 'eins'
        two = 'zwei'
    value2enum = dict((e.value, e) for e in FooEnum.__members__.values())

    value_column = Column('value', ValuesEnum(FooEnum))
    table = db_ctx.init_table_with_values([value_column], [{'value': value}])
    expected_enum = value2enum.get(value)
    assert db_ctx.fetch_db_value(table) == value
    assert db_ctx.fetch_value(table) == expected_enum


def test_values_enum_can_store_and_load_int_values(db_ctx):
    NrConsts = Enum('NrConsts', ('ONE', 'TWO'))
    assert NrConsts.ONE.value == 1

    value_column = Column('value', ValuesEnum(NrConsts))
    table = db_ctx.init_table_with_values([value_column], [{'value': NrConsts.ONE}])
    assert db_ctx.fetch_db_value(table) == '1'
    assert db_ctx.fetch_value(table) == NrConsts.ONE
