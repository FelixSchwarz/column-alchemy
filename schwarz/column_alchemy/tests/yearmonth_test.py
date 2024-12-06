# -*- coding: utf-8 -*-
# Copyright (c) 2017, 2019-2021, 2023, 2024 Felix Schwarz
# The source code contained in this file is licensed under the MIT license.
# SPDX-License-Identifier: MIT

from datetime import date as Date

import pytest

from ..yearmonth import YearMonth


def test_can_compare_with_greater():
    assert YearMonth(2017, 12) > YearMonth(2016, 1)
    assert YearMonth(2017, 1) > YearMonth(2016, 12)
    assert YearMonth(2017, 5) > YearMonth(2017, 4)

    assert not (YearMonth(2016, 1) > YearMonth(2017, 12))
    assert not (YearMonth(2016, 12) > YearMonth(2017, 1))
    assert not (YearMonth(2017, 4) > YearMonth(2017, 5))

def test_can_compare_with_greater_or_equal():
    assert YearMonth(2017, 12) >= YearMonth(2016, 1)
    assert YearMonth(2017, 1) >= YearMonth(2016, 12)
    assert not (YearMonth(2016, 1) >= YearMonth(2017, 12))
    assert not (YearMonth(2016, 12) >= YearMonth(2017, 1))

def test_can_compare_with_lower():
    assert YearMonth(2016, 1) < YearMonth(2017, 12)
    assert YearMonth(2016, 12) < YearMonth(2017, 1)
    assert YearMonth(2017, 4) < YearMonth(2017, 5)
    assert not (YearMonth(2017, 12) < YearMonth(2016, 1))
    assert not (YearMonth(2017, 1) < YearMonth(2016, 12))
    assert not (YearMonth(2017, 5) < YearMonth(2017, 4))

def test_can_compare_with_lower_or_equal():
    assert YearMonth(2016, 1) <= YearMonth(2017, 12)
    assert YearMonth(2016, 12) <= YearMonth(2017, 1)
    assert not (YearMonth(2017, 12) <= YearMonth(2016, 1))
    assert not (YearMonth(2017, 1) <= YearMonth(2016, 12))

@pytest.mark.parametrize('month', [0, 13])
def test_rejects_invalid_months(month):
    with pytest.raises(ValueError):
        YearMonth(2019, month)

def test_can_return_current_month():
    today = Date.today()
    current_month = YearMonth(today.year, today.month)
    assert YearMonth.current_month() == current_month

def test_can_return_previous_month():
    assert YearMonth(2020, 1).previous_month() == YearMonth(2019, 12)

def test_can_return_next_month():
    assert YearMonth(2019, 1).next_month() == YearMonth(2019, 2)
    assert YearMonth(2019, 12).next_month() == YearMonth(2020, 1)

def test_can_return_str():
    assert str(YearMonth(2020, 1)) == '01/2020'
    assert str(YearMonth(2019, 12)) == '12/2019'

def test_can_parse_str():
    ym = YearMonth(2021, 2)
    assert YearMonth.from_str('02/2021') == ym
    assert YearMonth.from_str('2/2021') == ym
    assert YearMonth.from_str(str(ym)) == ym
    assert YearMonth.from_str('2021-02') == ym


def test_contains():
    assert Date(2024, 3, 1) in YearMonth(2024, 3)
    assert Date(2024, 3, 31) in YearMonth(2024, 3)
    assert Date(2024, 4, 1) not in YearMonth(2024, 3)
    assert Date(2024, 2, 29) not in YearMonth(2024, 3)
    assert YearMonth(2024, 3) not in YearMonth(2024, 3)
