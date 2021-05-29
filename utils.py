import json
import logging
import os.path

import config

SECONDS_IN_MONTH = 60 * 60 * 24 * 30
COMPARISON_POINT = 20 * 60  # Minutes until 8PM


def list_to_chunks(list_to_split, chunk_length):
    """
    Split list l to sublists of length n
    """
    for i in range(0, len(list_to_split), chunk_length):
        yield list_to_split[i:i + chunk_length]


def get_json_from_file(file_name=config.DEFAULT_FILE):
    """
    Get json from file by filename
    """
    if not os.path.isfile(file_name):
        logging.error(f"no such file: {file_name}")
        exit(1)

    file = open(file_name, "r")
    try:
        json_in_file = json.loads(file.read())
        return json_in_file
    except:
        logging.error(f"Invalid json inside file: {file_name}")
        exit(1)
