from sqlalchemy.sql.expression import func, literal

from pygotham_2019 import meta, model
from pygotham_2019.utils import print_table


if __name__ == "__main__":
    meta.session.add_all([
      model.Record(tags=["defect", "minor_change", "backend"]),
      model.Record(tags=["defect", "major_change", "backend"]),
      model.Record(tags=["enhancement", "ui/ux", "frontend"]),
    ])
    meta.session.flush()

    records = (
        meta.session.query(model.Record)
            .filter(model.Record.tags.op("&&")(["defect", "backend"]))
    )

    print("filtering with &&")
    print_table(records)
    print("")

    counts = (
        meta.session.query(
            func.unnest(model.Record.tags).label("tag"),
            func.count().label("count"),
        )
        .group_by(literal(1))
        .order_by(literal(2).desc(), literal(1))
    )

    print("unnest and counting tags")
    print_table(counts)
