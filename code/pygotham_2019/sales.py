import random
from decimal import Decimal, ROUND_HALF_UP

from faker import Faker

from pygotham_2019 import meta, model


def setup():
    random.seed(0)

    fake = Faker()

    store_ids = [
        "EAST-NY-12345",
        "EAST-NY-22222",
        "EAST-NY-55555",
        "WEST-CA-55555",
        "WEST-AZ-55555",
        "SOUT-GA-11111",
        "SOUT-AL-54321",
        "NORT-MN-44444",
    ]

    items = [
        "Bananaphone",
        "Cat Selfie Duct Tape",
        "Always Listening Voice Assistant",
        "Jimmies Guide to Programming",
    ]

    for _ in range(1000):

        store_id = random.choice(store_ids)
        item = random.choice(items)

        amount = Decimal(random.random() * 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        date = fake.date_between(start_date="-3y", end_date="now")

        meta.session.add(
            model.Sale(
                item=item,
                amount=amount,
                store_id=store_id,
                date=date,
            ),
        )

    meta.session.flush()
