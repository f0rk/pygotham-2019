from sqlalchemy.sql.expression import func, literal

from pygotham_2019 import meta, model
from pygotham_2019.utils import print_table


if __name__ == "__main__":

    # some sort of generic record object with tags. imagine these to be tickets
    # in an issue tracking system
    meta.session.add_all([
      model.Record(tags=["defect", "minor_change", "backend"]),
      model.Record(tags=["defect", "major_change", "backend"]),
      model.Record(tags=["enhancement", "ui/ux", "frontend"]),
    ])
    meta.session.flush()

    # filter the result with &&, the overlaps operator, which says "if either
    # of these two arrays have any elements in common, include them in the
    # output". works like checking against a non-empty set intersection.
    records = (
        meta.session.query(model.Record)
            .filter(model.Record.tags.op("&&")(["defect", "backend"]))
    )

    print("filtering with &&")
    print_table(records)
    print("")

    # unnest takes the array and expands it into rows. this allows you to, for
    # example, calculate statistics on tags, find unique tags, etc.
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
