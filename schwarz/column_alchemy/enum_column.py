# -*- coding: utf-8 -*-
# Copyright (c) 2017 Felix Schwarz
# The source code contained in this file is licensed under the MIT license.
# SPDX-License-Identifier: MIT

from sqlalchemy.types import Enum as SQLEnum


__all__ = ['ValuesEnum']

class ValuesEnum(SQLEnum):
    """This is pretty similar to SQLAlchemy's Enum type.
    However SQLAlchemy stores the NAMES of enum options in the databases
    instead of their associated values.

        class Foo(Enum):
            one = 'eins'
            two = 'zwei'

    SQLAlchemy's Enum stores 'one'/'two' in the database not 'eins'/'zwei'.
    This has two advantages:
    - names can be serialized to strings easily while enum values can be
      arbitrary Python types without bijective serialization.
    - Enum values are not necessarily unique (unless @unique is used)

    However I found SQLAlchemy's behaviour highly confusing as I tend use
    enum names similar to variable names to provide better code readability.
    This class will store the enum VALUES in the database.

    Currently this is really a bare-bones implementation so it comes with two
    important limitations:
    1. Enum values must be unique. No effort is made to ensure that this is
       really the case.
    2. Enum values must be strings.
    """
    # override SQLAlchemy's Enum._parse_into_values()
    def _parse_into_values(self, enums, kw):
        if len(enums) == 1 and hasattr(enums[0], '__members__'):
            self.enum_class = enums[0]
            objects = tuple(self.enum_class.__members__.values())
            values = [o.value for o in objects]
            kw.setdefault('name', self.enum_class.__name__.lower())
            return values, objects
        else:
            self.enum_class = None
            return enums, enums
