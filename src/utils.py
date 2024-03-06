import json
import sys

import jsast


def create_ast(**kwargs):
    cls_type = kwargs.pop('type')
    if 'async' in kwargs: kwargs["is_async"] = kwargs.pop("async")
    n = getattr(jsast, cls_type)
    return n(**kwargs)


def parse_program(filename):
    with open(filename, "r") as f:
        r = json.load(f, object_hook=lambda d: create_ast(**d))
    return jsast.BlockStatement(body=r.program.body, directives=[])


if __name__ == "__main__":
    parse_program(sys.argv[1])
