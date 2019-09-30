from sqlalchemy import Column, Date, Integer, Numeric, Text
from sqlalchemy.dialects.postgresql import ARRAY, DATERANGE

from pygotham_2019 import meta


class Record(meta.Base):

    __tablename__ = "records"

    id = Column(Integer, primary_key=True)
    tags = Column(ARRAY(Text))


class DrugInfo(meta.Base):

    __tablename__ = "drug_info"

    id = Column(Text, primary_key=True)
    validity = Column(DATERANGE, primary_key=True) # XXX: could be better
    name = Column(Text)
    description = Column(Text)


class DrugPrice(meta.Base):

    __tablename__ = "drug_prices"

    id = Column(Text, primary_key=True)
    validity = Column(DATERANGE, primary_key=True)
    unit_price = Column(Numeric)


class Sale(meta.Base):

    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    item = Column(Text)
    amount = Column(Numeric)
    store_id = Column(Text)
