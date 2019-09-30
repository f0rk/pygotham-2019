import datetime
from decimal import Decimal

from psycopg2.extras import DateRange
from sqlalchemy.sql.expression import and_, func

from pygotham_2019 import meta, model
from pygotham_2019.utils import print_table


if __name__ == "__main__":

    meta.session.add_all([
        model.DrugInfo(
            id="1234567890",
            validity=DateRange(
                lower="1970-01-01",
                upper="2019-10-04",
            ),
            name="Lipitor",
            description="20mg tablet",
        ),
        model.DrugInfo(
            id="1234567890",
            validity=DateRange(
                lower="2019-10-04",
                upper="9999-12-31",
            ),
            name="Lipitor",
            description="20mg Tablet",
        ),
        model.DrugInfo(
            id="9999999999",
            validity=DateRange(
                lower="1970-01-01",
                upper="9999-12-31",
            ),
            name="Crestor",
            description="20mg capsule",
        ),
    ])
    meta.session.flush()

    drugs = (
        meta.session.query(model.DrugInfo)
            .filter(model.DrugInfo.validity.op("@>")(func.current_date()))
    )

    print("filtering with range types, current time")
    print_table(drugs)
    print("")

    drugs = (
        meta.session.query(model.DrugInfo)
            .filter(model.DrugInfo.validity.op("@>")(datetime.date(2019, 1, 1)))
    )

    print("filtering with range types, explicit date")
    print_table(drugs)
    print("")

    meta.session.add_all([
        model.DrugPrice(
            id="1234567890",
            validity=DateRange(
                lower="1970-01-01",
                upper="2019-01-01",
            ),
            unit_price=Decimal("12.00"),
        ),
        model.DrugPrice(
            id="1234567890",
            validity=DateRange(
                lower="2019-01-01",
                upper="2019-03-01",
            ),
            unit_price=Decimal("13.00"),
        ),
        model.DrugPrice(
            id="1234567890",
            validity=DateRange(
                lower="2019-03-01",
                upper="2019-10-01",
            ),
            unit_price=Decimal("14.00"),
        ),
        model.DrugPrice(
            id="1234567890",
            validity=DateRange(
                lower="2019-10-01",
                upper="9999-12-31",
            ),
            unit_price=Decimal("15.00"),
        ),
        model.DrugPrice(
            id="9999999999",
            validity=DateRange(
                lower="1970-01-01",
                upper="2019-02-01",
            ),
            unit_price=Decimal("80.00"),
        ),
        model.DrugPrice(
            id="9999999999",
            validity=DateRange(
                lower="2019-02-01",
                upper="2019-08-01",
            ),
            unit_price=Decimal("90.00"),
        ),
        model.DrugPrice(
            id="9999999999",
            validity=DateRange(
                lower="2019-08-01",
                upper="9999-12-31",
            ),
            unit_price=Decimal("100.00"),
        ),
    ])
    meta.session.flush()

    drugs_and_prices = (
        meta.session.query(model.DrugInfo, model.DrugPrice)
        .join(
            model.DrugPrice,
            and_(
                model.DrugInfo.id == model.DrugPrice.id,
                model.DrugInfo.validity.op("&&")(model.DrugPrice.validity),
            ),
        )
        .order_by(model.DrugInfo.id, model.DrugInfo.validity, model.DrugPrice.validity)
    )

    print("join over ranges")
    print_table(drugs_and_prices)
    print("")

    drugs_and_prices = (
        drugs_and_prices
        .filter(model.DrugInfo.validity.op("@>")(datetime.date(2019, 8, 1)))
        .filter(model.DrugPrice.validity.op("@>")(datetime.date(2019, 8, 1)))
    )

    print("join over ranges, with filtering")
    print_table(drugs_and_prices)
