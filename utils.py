import json

import config

SECONDS_IN_MONTH = 60 * 60 * 24 * 30


def list_to_chunks(l, n):
    """
    Split list l to sublists of length n
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_json_from_file(file = config.DEFAULT_FILE):
    file = open(file, "r")
    json_in_file = json.loads(file.read())
    file.close()
    return json_in_file