from sqlalchemy.sql.expression import func, literal

from pygotham_2019 import meta, model, sales
from pygotham_2019.utils import print_table


if __name__ == "__main__":

    sales.setup()

    sales_report = (
        meta.session.query(
            func.left(model.Sale.store_id, 4).label("region"),
            func.left(model.Sale.store_id, 7).label("state"),
            model.Sale.store_id.label("store"),
            func.sum(model.Sale.amount).label("sales_for_store"),
        )
        .group_by(
            func.grouping_sets(
                func.left(model.Sale.store_id, 4),
                func.left(model.Sale.store_id, 7),
                model.Sale.store_id,
            )
        )
    )

    print("grouping sets to compute aggregates at multiple levels")
    print_table(sales_report)
    print("")

    sales_report = (
        meta.session.query(
            func.left(model.Sale.store_id, 4).label("region"),
            func.left(model.Sale.store_id, 7).label("state"),
            model.Sale.store_id.label("store"),
            func.sum(model.Sale.amount).label("sales_for_store"),
        )
        .group_by(
            func.rollup(
                func.left(model.Sale.store_id, 4),
                func.left(model.Sale.store_id, 7),
                model.Sale.store_id,
            )
        )
    )

    print("rollup to compute aggregates at multiple levels")
    print_table(sales_report)
