# -*- coding: utf-8 -*-
# Copyright (c) 2017, 2019-2021 Felix Schwarz
# The source code contained in this file is licensed under the MIT license.
# SPDX-License-Identifier: MIT

from datetime import date as Date

from ddt import ddt as DataDrivenTestCase, data as ddt_data
from pythonic_testcase import *

from ..yearmonth import YearMonth


@DataDrivenTestCase
class YearMonthTest(PythonicTestCase):
    def test_can_compare_with_greater(self):
        assert_true(YearMonth(2017, 12) > YearMonth(2016, 1))
        assert_true(YearMonth(2017, 1) > YearMonth(2016, 12))
        assert_true(YearMonth(2017, 5) > YearMonth(2017, 4))

        assert_false(YearMonth(2016, 1) > YearMonth(2017, 12))
        assert_false(YearMonth(2016, 12) > YearMonth(2017, 1))
        assert_false(YearMonth(2017, 4) > YearMonth(2017, 5))

    def test_can_compare_with_greater_or_equal(self):
        assert_true(YearMonth(2017, 12) >= YearMonth(2016, 1))
        assert_true(YearMonth(2017, 1) >= YearMonth(2016, 12))
        assert_false(YearMonth(2016, 1) >= YearMonth(2017, 12))
        assert_false(YearMonth(2016, 12) >= YearMonth(2017, 1))

    def test_can_compare_with_lower(self):
        assert_true(YearMonth(2016, 1) < YearMonth(2017, 12))
        assert_true(YearMonth(2016, 12) < YearMonth(2017, 1))
        assert_true(YearMonth(2017, 4) < YearMonth(2017, 5))
        assert_false(YearMonth(2017, 12) < YearMonth(2016, 1))
        assert_false(YearMonth(2017, 1) < YearMonth(2016, 12))
        assert_false(YearMonth(2017, 5) < YearMonth(2017, 4))

    def test_can_compare_with_lower_or_equal(self):
        assert_true(YearMonth(2016, 1) <= YearMonth(2017, 12))
        assert_true(YearMonth(2016, 12) <= YearMonth(2017, 1))
        assert_false(YearMonth(2017, 12) <= YearMonth(2016, 1))
        assert_false(YearMonth(2017, 1) <= YearMonth(2016, 12))

    @ddt_data(0, 13)
    def test_rejects_invalid_months(self, month):
        with assert_raises(ValueError, message='invalid month "%d"' % month):
            YearMonth(2019, month)

    def test_can_return_current_month(self):
        today = Date.today()
        current_month = YearMonth(today.year, today.month)
        assert_equals(current_month, YearMonth.current_month())

    def test_can_return_previous_month(self):
        assert_equals(YearMonth(2019, 12), YearMonth(2020, 1).previous_month())

    def test_can_return_next_month(self):
        assert_equals(YearMonth(2019, 2), YearMonth(2019, 1).next_month())
        assert_equals(YearMonth(2020, 1), YearMonth(2019, 12).next_month())

    def test_can_return_str(self):
        assert_equals('01/2020', str(YearMonth(2020, 1)))
        assert_equals('12/2019', str(YearMonth(2019, 12)))

    def test_can_parse_str(self):
        ym = YearMonth(2021, 2)
        assert_equals(ym, YearMonth.from_str('02/2021'))
        assert_equals(ym, YearMonth.from_str(str(ym)))
        assert_equals(ym, YearMonth.from_str('2021-02'))

