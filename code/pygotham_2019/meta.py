import os
from collections import OrderedDict

from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(
    os.environ["PYGOTHAM_2019_DB_URL"],
    use_batch_mode=True,
    pool_timeout=5,
)
session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    ),
)


class Base(object):

    def __json__(self):
        def maybe_convert(v: any):
            if hasattr(v, "__json__"):
                return v.__json__()
            else:
                return v

        ret = OrderedDict()
        for attr in inspect(self).attrs.keys():
            val = getattr(self, attr)

            if isinstance(val, list):
                ret[attr] = []
                for v in val:
                    ret[attr].append(maybe_convert(v))
            else:
                ret[attr] = maybe_convert(val)

        return ret


Base = declarative_base(cls=Base)
