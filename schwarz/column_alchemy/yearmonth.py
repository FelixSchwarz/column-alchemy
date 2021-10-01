# -*- coding: utf-8 -*-
# Copyright (c) 2017, 2019-2021 Felix Schwarz
# The source code contained in this file is licensed under the MIT license.
# SPDX-License-Identifier: MIT

import calendar
from datetime import date as Date, timedelta as TimeDelta
import functools
import re


__all__ = ['YearMonth']

@functools.total_ordering
class YearMonth(object):
    def __init__(self, year, month):
        self.year = year
        self.month = month
        # this raises a ValueError if month is not with 1..12
        Date(self.year, self.month, 1)

    @classmethod
    def from_iso_string(cls, iso_str):
        year_str, month_str = iso_str.split('-', 1)
        return YearMonth(int(year_str), int(month_str))

    def as_iso_string(self):
        return '%04d-%02d' % (self.year, self.month)

    @classmethod
    def from_str(cls, month_str):
        assert len(month_str) == 7
        iso_pattern = r'^\d{4}\-\d{2}$'
        if re.match(iso_pattern, month_str):
            return cls.from_iso_string(month_str)

        str_pattern = r'^(\d{2})/(\d{4})$'
        m = re.match(str_pattern, month_str)
        if m:
            month_str, year_str = m.groups()
            return YearMonth(int(year_str), int(month_str))
        raise ValueError('unable to parse %r' % month_str)

    @classmethod
    def from_int(cls, int_value):
        int_str = str(int_value)
        assert len(int_str) == 6
        year_str = int_str[:4]
        month_str = int_str[4:]
        return YearMonth(int(year_str), int(month_str))

    def as_int(self):
        return int(self.as_compressed_string())

    def as_compressed_string(self, two_digit_year=None, full_year=None):
        if (two_digit_year is None) and (full_year is None):
            full_year = True
        assert (bool(two_digit_year) ^ bool(full_year))
        if full_year:
            two_digit_year = False

        year_str = str(self.year)
        if two_digit_year:
            year_str = year_str[2:4]
        return '%s%02d' % (year_str, self.month)

    @classmethod
    def from_date(cls, date):
        return YearMonth(date.year, date.month)

    def as_date(self, day):
        return Date(self.year, self.month, day)

    def first_date_of_month(self):
        return self.as_date(day=1)

    def last_date_of_month(self):
        weekday_first_day, nr_days_in_month = calendar.monthrange(self.year, self.month)
        return self.as_date(day=nr_days_in_month)

    @classmethod
    def current_month(cls):
        return YearMonth.from_date(Date.today())

    def previous_month(self):
        end_of_previous_month = self.first_date_of_month() - TimeDelta(days=1)
        return YearMonth.from_date(end_of_previous_month)

    def next_month(self):
        start_of_next_month = self.last_date_of_month() + TimeDelta(days=1)
        return YearMonth.from_date(start_of_next_month)

    def __str__(self):
        return '%02d/%d' % (self.month, self.year)

    def __repr__(self):
        klassname = self.__class__.__name__
        return '%s(%r, %r)' % (klassname, self.year, self.month)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        if not (hasattr(other, 'year') and hasattr(other, 'month')):
            return False
        elif hasattr(other, 'day'):
            # I think Date(2017, 4, 1) should not be equal to YearMonth(2017, 4)
            return False
        return (self.year == other.year) and (self.month == other.month)

    def __lt__(self, other):
        if self.year != other.year:
            return (self.year < other.year)
        return (self.month < other.month)


