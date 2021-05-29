import json

import config

SECONDS_IN_MONTH = 60 * 60 * 24 * 30
COMPARISON_POINT = 20 * 60  # Minutes until 8PM


def list_to_chunks(list_to_split, chunk_length):
    """
    Split list l to sublists of length n
    """
    for i in range(0, len(list_to_split), chunk_length):
        yield list_to_split[i:i + chunk_length]


def get_json_from_file(file=config.DEFAULT_FILE):
    file = open(file, "r")
    json_in_file = json.loads(file.read())
    file.close()
    return json_in_file
