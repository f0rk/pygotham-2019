from sqlalchemy.sql.expression import func, literal

from pygotham_2019 import meta, model, sales
from pygotham_2019.utils import print_table


if __name__ == "__main__":

    sales.setup()

    sales_by_store = (
        meta.session.query(
            model.Sale.store_id.label("store_id"),
            func.sum(model.Sale.amount).label("amount"),
        )
        .group_by(literal(1))
    ).cte("stores")

    sales_report = (
        meta.session.query(
            func.left(sales_by_store.c.store_id, 4).label("region"),
            func.sum(sales_by_store.c.amount).over(partition_by=func.left(sales_by_store.c.store_id, 4)).label("sales_for_region"),
            func.left(sales_by_store.c.store_id, 7).label("state"),
            func.sum(sales_by_store.c.amount).over(partition_by=func.left(sales_by_store.c.store_id, 7)).label("sales_for_state"),
            sales_by_store.c.store_id.label("store"),
            sales_by_store.c.amount.label("sales_for_store"),
        )
        .order_by(
            literal(2).desc(),
            literal(4).desc(),
            literal(6).desc(),
        )
    )

    print("window functions to compute aggregates at multiple levels")
    print_table(sales_report)
