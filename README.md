
This repo contains a **custom column types for SQLAlchemy** which I use in different projects.

The code should be compatible with SQLAlchemy 1.3.x.


UTCDateTime
-----------

`UTCDateTime` stores a Python tz-aware `datetime.datetime` value as UTC datetime in the database (without explicit timezone information). I use this to introduce tz-aware timezones in systems which expect "naive" datetimes in the database.

    from schwarz.column_alchemy import UTCDateTime

    class Foo(Base)
        __tablename__ = 'foo'
        id = Column(Integer, autoincrement=True, primary_key=True)
        timestamp = Column(UTCDateTime)
    


ValuesEnum
-----------
TODO

IntValuesEnum
-------------
TODO

