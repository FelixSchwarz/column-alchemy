# -*- coding: utf-8 -*-
# Copyright (c) 2017, 2019, 2020 Felix Schwarz
# The source code contained in this file is licensed under the MIT license.
# SPDX-License-Identifier: MIT

from datetime import date as Date

from pythonic_testcase import *

from ..yearmonth import YearMonth


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

    def test_can_return_current_month(self):
        today = Date.today()
        current_month = YearMonth(today.year, today.month)
        assert_equals(current_month, YearMonth.current_month())

    def test_can_return_previous_month(self):
        assert_equals(YearMonth(2019, 12), YearMonth(2020, 1).previous_month())

    def test_can_return_str(self):
        assert_equals('01/2020', str(YearMonth(2020, 1)))
        assert_equals('12/2019', str(YearMonth(2019, 12)))

