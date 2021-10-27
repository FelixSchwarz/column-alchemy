
This repo contains a **custom column types for SQLAlchemy** which I use in different projects.

The code should be compatible with SQLAlchemy 1.2.3 - 1.4.x.

    pip install ColumnAlchemy


UTCDateTime
-----------

`UTCDateTime` stores a Python tz-aware `datetime.datetime` value as UTC datetime in the database (without explicit timezone information). I use this to introduce tz-aware timezones in systems which expect "naive" datetimes in the database.

    from schwarz.column_alchemy import UTCDateTime

    class Foo(Base)
        __tablename__ = 'foo'
        id = Column(Integer, autoincrement=True, primary_key=True)
        timestamp = Column(UTCDateTime)


ShiftedDecimal
--------------

`ShiftedDecimal` stores a `Decimal` as integer in the database (with limited precision). This is especially useful to store decimal values even in sqlite which requires special treatment to store decimals.

    from decimal import Decimal
    from schwarz.column_alchemy import ShiftedDecimal

    class Foo(Base)
        __tablename__ = 'foo'
        id = Column(Integer, autoincrement=True, primary_key=True)
        percentage = Column(ShiftedDecimal(4))
    
    foo = Foo(percentage=Decimal('1.2324'))
    # stores percentage as 12324 in the database but returns the
    # correct Decimal value after loading.


ValuesEnum
-----------
TODO

IntValuesEnum
-------------
TODO


YearMonthColumn
---------------

`YearMonth` is similar to `datetime.date` but without a `day` attribute. It can be used to represent a calendar month and provides some convenience methods like `first_date_of_month()` and `last_date_of_month()`. A **`YearMonthColumn`** stores a `YearMonth` instance as "YYYY-MM" in the database.

    from schwarz.column_alchemy import YearMonth, YearMonthColumn

    class Foo(Base)
        __tablename__ = 'foo'
        id = Column(Integer, autoincrement=True, primary_key=True)
        month = Column(YearMonthColumn())

    foo = Foo(month=YearMonth(2020, 7))
    # stores "month" as "2020-07" in the database but returns a
    # YearMonth instance after loading.


YearMonthIntColumn
------------------

Very similar to `YearMonthColumn` but stores `YearMonth(2020, 7)` as `202007` (integer).

