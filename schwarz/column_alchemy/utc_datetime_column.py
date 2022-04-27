# -*- coding: utf-8 -*-
# Copyright 2013, 2018 Felix Schwarz
# The source code in this file is is dual licensed under the MIT license or
# the GPLv3 or (at your option) any later version.
# SPDX-License-Identifier: MIT or GPL-3.0-or-later

from datetime import datetime

from babel.dates import UTC
from sqlalchemy.types import DateTime, TypeDecorator


__all__ = ['UTCDateTime']

# -----------------------------------------------------------------------------
# copied from http://stackoverflow.com/a/2528453/138526
# but modified so that the timezone information is stripped by default before
# passing the value to the DB. This prevents a MySQLdb warning
# Warning: Incorrect datetime value: '<dt with tz>' for column 'date' at row 1

class UTCDateTime(TypeDecorator):
    impl = DateTime
    cache_ok = True

    def __init__(self, *args, **kwargs):
        self._strip_tz = kwargs.pop('strip_tz', True)
        super(UTCDateTime, self).__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if value.tzinfo is None:
            # since Python 3.6 ".astimetzone()" also works on naive datetime
            # instances so we have to check this separately.
            raise ValueError('naive datetime instance passed: %r' % value)
        utc_dt = value.astimezone(UTC)
        if self._strip_tz:
            return utc_dt.replace(tzinfo=None)
        return utc_dt

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return datetime(value.year, value.month, value.day,
                        value.hour, value.minute, value.second,
                        value.microsecond, tzinfo=UTC)
# -----------------------------------------------------------------------------

