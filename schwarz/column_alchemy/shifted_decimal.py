# -*- coding: utf-8 -*-
# Copyright (c) 2017 Felix Schwarz
# The source code contained in this file is licensed under the MIT license.
# SPDX-License-Identifier: MIT
#
# Basic idea and initial code from Michael Bayer as part of the SQLAlchemy
# project:
# https://bitbucket.org/zzzeek/sqlalchemy/issues/1759/sqlite-support-for-arbitrary-precision#comment-9011277

from __future__ import absolute_import, print_function, unicode_literals

from decimal import Decimal

from sqlalchemy.types import Integer, TypeDecorator


__all__ = ['numeric_to_db_int', 'ShiftedDecimal']

def numeric_to_db_int(number, scale):
    if number is None:
        return None
    elif isinstance(number, Decimal):
        db_number = number.shift(scale)
        if int(db_number) != db_number:
            raise ValueError('%r has too many decimal places (only %d stored in DB)' % (number, scale))
    else:
        # e.g. plain integers
        db_number = number * Decimal('1E+%d' % scale)
    return int(db_number)


class ShiftedDecimal(TypeDecorator):
    impl = Integer

    def __init__(self, scale=2):
        TypeDecorator.__init__(self)
        self.scale = scale

    def process_bind_param(self, value, dialect):
        return numeric_to_db_int(value, self.scale)

    def process_result_value(self, value, dialect):
        if value is not None:
            value = value * Decimal('1E-%d' % self.scale)
        return value

    def copy(self):
        return ShiftedDecimal(scale=self.scale)

