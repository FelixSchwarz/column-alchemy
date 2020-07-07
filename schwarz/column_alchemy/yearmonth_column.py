# -*- coding: utf-8 -*-
# Copyright (c) 2017 Felix Schwarz
# The source code contained in this file is licensed under the MIT license.
# SPDX-License-Identifier: MIT
#
# Basic idea and initial code from Michael Bayer / SQLAlchemy project

from sqlalchemy.types import Integer, String, TypeDecorator

from .yearmonth import YearMonth


__all__ = ['YearMonthColumn', 'YearMonthIntColumn']

class YearMonthColumn(TypeDecorator):
    impl = String(7)

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return value.as_iso_string()

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return YearMonth.from_iso_string(value)

    def copy(self):
        return YearMonthColumn()


class YearMonthIntColumn(TypeDecorator):
    impl = Integer

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        elif hasattr(value, 'as_int'):
            return value.as_int()
        # probably "value" is already an int.
        # I think this happens if SQLAlchemy tries to join columns by itself.
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return YearMonth.from_int(value)

    def copy(self):
        return YearMonthIntColumn()
