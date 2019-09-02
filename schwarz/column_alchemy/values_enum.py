# -*- coding: utf-8 -*-
# Copyright (c) 2017, 2019 Felix Schwarz
# The source code contained in this file is licensed under the MIT license.
# SPDX-License-Identifier: MIT

from sqlalchemy.types import Enum as SQLEnum


__all__ = [
    'get_enum_value',
    'ValuesEnum',
]

def ValuesEnum(enum_class, **enum_kwargs):
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

    However I found SQLAlchemy's default behaviour highly confusing as I tend
    use enum names similar to variable names to provide better code readability.
    Often I like to to store the enum VALUES in the database.

    SQLAlchemy >= 1.2.3 introduced the "values_callable" parameter so there is
    no need for a custom column implementation. However this module provides
    some nice helpers so there is no code duplication across different projects.

    The current implementation is pretty basic so it comes with two
    important limitations:
    1. Enum values must be unique. No effort is made to ensure that this is
       really the case.
    2. Enum values must be strings.
    """
    return SQLEnum(enum_class, values_callable=get_enum_values, **enum_kwargs)


def get_enum_value(enum_obj):
    # Ad-hoc instances (not loaded from SQLAlchemy) do not have a real
    # enum instance. In these cases we get a plain string which represents the
    # wanted value.
    value = enum_obj.value if hasattr(enum_obj, 'value') else enum_obj
    return value

def get_enum_values(enum_class):
    return [item.value for item in enum_class]

