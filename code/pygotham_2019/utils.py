from collections import OrderedDict

from tabulate import tabulate

from pygotham_2019 import meta


def _flatten(flattened, result, key=None):

    def _prefix_key(l):
        if key is not None:
            return "{}.{}".format(key, l)
        else:
            return l

    if hasattr(result, "_asdict"):
        asdict = result._asdict()

        for local_key, item in asdict.items():
            if hasattr(item, "_asdict"):
                _flatten(flattened, item, key=_prefix_key(local_key))
            if hasattr(item, "__json__"):
                _flatten(flattened, [item], key=_prefix_key(local_key))
            else:
                flattened[_prefix_key(local_key)] = item
    else:
        for item in result:
            if hasattr(item, "_asdict"):
                _flatten(flattened, item)
            if hasattr(item, "__json__"):
                for local_key, value in item.__json__().items():
                    flattened[_prefix_key(local_key)] = value
            elif hasattr(item, "keys"):
                for local_key in item.keys():
                    flattened[_prefix_key(local_key)] = item[local_key]
            else:
                flattened[key] = item


def print_table(results):

    data = []
    headers = []
    for result in results:

        if isinstance(result, meta.Base):
            result = [result]

        flattened = OrderedDict()
        _flatten(flattened, result)

        if not headers:
            headers = list(flattened.keys())

        data.append(list(flattened.values()))

    print(tabulate(data, headers=headers, tablefmt="psql"))
