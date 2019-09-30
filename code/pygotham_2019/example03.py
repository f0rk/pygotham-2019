from sqlalchemy.sql.expression import func, literal

from pygotham_2019 import meta, model, sales
from pygotham_2019.utils import print_table


if __name__ == "__main__":

    sales.setup()

    sales_by_region = (
        meta.session.query(
            func.left(model.Sale.store_id, 4).label("region"),
            func.sum(model.Sale.amount).label("amount"),
        )
        .group_by(literal(1))
    ).cte("regions")

    sales_by_state = (
        meta.session.query(
            func.left(model.Sale.store_id, 7).label("state"),
            func.sum(model.Sale.amount).label("amount"),
        )
        .group_by(literal(1))
    ).cte("states")

    sales_by_store = (
        meta.session.query(
            model.Sale.store_id.label("store_id"),
            func.left(model.Sale.store_id, 7).label("state"),
            func.left(model.Sale.store_id, 4).label("region"),
            func.sum(model.Sale.amount).label("amount"),
        )
        .group_by(literal(1), literal(2), literal(3))
    ).cte("stores")

    sales_report = (
        meta.session.query(
            sales_by_region.c.region.label("region"),
            sales_by_region.c.amount.label("sales_for_region"),
            sales_by_state.c.state.label("state"),
            sales_by_state.c.amount.label("sales_for_state"),
            sales_by_store.c.store_id.label("store"),
            sales_by_store.c.amount.label("sales_for_store"),
        )
        .select_from(sales_by_store)
        .join(
            sales_by_state,
            sales_by_state.c.state == sales_by_store.c.state,
        )
        .join(
            sales_by_region,
            sales_by_region.c.region == sales_by_store.c.region,
        )
        .order_by(
            sales_by_region.c.amount.desc(),
            sales_by_state.c.amount.desc(),
            sales_by_store.c.amount.desc(),
        )
    )

    print("common table expressions to compute aggregates at multiple levels")
    print_table(sales_report)
