import json
from multiprocessing.pool import ThreadPool

import numpy as np
import requests

import config
from utils import list_to_chunks


def get_items(item_ids):
    """
    Get responses fot there item ids
    """
    items = []
    for item_id in item_ids:
        items.append(requests.get(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"))
    return items


def get_items_by_ids_with_threads(item_ids):
    """
    Using threads speeds up getting the titles.
    This is faster than doing it in 1 thread,
    but maybe less fun that seeing the articles show up 1 by 1
    """
    thread_amount = config.THREAD_POOL_SIZE
    rows_per_thread = int((item_ids.shape[0] / thread_amount) + 1)
    chunks_for_threads = list(list_to_chunks(item_ids, rows_per_thread))
    pool = ThreadPool(thread_amount)
    lists_responses = pool.map(get_items, chunks_for_threads)
    pool.close()
    pool.join()
    return [item for sublist in lists_responses for item in sublist]


def get_top_ids(amount=config.DEFAULT_TOP_POSTS_AMOUNT):
    """
    Return ids of top HN articles
    """
    response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    response_json = json.loads(response.text)
    top_posts = np.array(response_json[:amount])
    return top_posts


def show_top(amount=config.DEFAULT_TOP_POSTS_AMOUNT):
    """
    Print top articles (amount is also limited by the official API, currently 500
    """
    top_ids = get_top_ids(amount)
    response_items = get_items_by_ids_with_threads(top_ids)
    for i, response in enumerate(response_items):
        response_json = json.loads(response.text)
        print(f"{i + 1}. {response_json['title']}")
