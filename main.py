import json
from functools import partial
from multiprocessing.pool import ThreadPool

import numpy as np
import requests

import config

TECHNOLOGIES = ['Kubernetes', 'Linux', 'Windows', 'Solarwinds', 'Garmin', 'AWS', 'Docker', 'Github', 'Wordpress',
                'Rundeck']
SECONDS_IN_MONTH = 60 * 60 *24 * 30

def list_to_chunks(l, n):
    """
    Split list l to sublists of length n
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_items(item_ids):
    """
    item ids to responses
    """
    items = []
    for id in item_ids:
        items.append(requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json"))
    return items


def get_items_by_ids_with_threads(item_ids):
    """
    Using threads speeds up getting the titles
    """
    thread_amount = config.THREAD_POOL_SIZE
    rows_per_thread = int((item_ids.shape[0] / thread_amount) + 1)
    # logger.log(level=0, msg="rows per thread: " + str(rows_per_thread))

    #  Divide entire workload of requests to {thread_amount} threads
    chunks_for_threads = list(list_to_chunks(item_ids, rows_per_thread))
    pool = ThreadPool(thread_amount)
    func = partial(get_items)
    lists_responses = pool.map(func, chunks_for_threads)
    pool.close()
    pool.join()
    return [item for sublist in lists_responses for item in sublist]


def show_top(amount=config.DEFAULT_TOP_POSTS_AMOUNT):
    top_ids = get_top_ids(amount)
    response_items = get_items_by_ids_with_threads(top_ids)
    for i in range(len(response_items)):
        response_json = json.loads(response_items[i].text)
        print(f"{i + 1}. {response_json['title']}")


def get_latest_titles(amount=config.DEFAULT_LATEST_AMOUNT):
    latest_ids = get_latest_ids(amount)
    response_items = get_items_by_ids_with_threads(latest_ids)
    for i in range(len(response_items)):
        response_json = json.loads(response_items[i].text)
        for tech in TECHNOLOGIES:
            if tech.lower() in response_json['title'].lower().split():
                print("boom", i, tech)


def get_latest_ids(amount=config.DEFAULT_LATEST_AMOUNT):
    response = requests.get("https://hacker-news.firebaseio.com/v0/newstories.json")
    response_json = json.loads(response.text)
    latest_posts = np.array(response_json[:amount])
    return latest_posts


def get_top_ids(amount=config.DEFAULT_TOP_POSTS_AMOUNT):
    response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    response_json = json.loads(response.text)
    top_posts = np.array(response_json[:amount])
    return top_posts


def get_json_from_file():
    file = open("hacker_news_data.json", "r")
    json_in_file = json.loads(file.read())
    file.close()
    return json_in_file


def learn_stuff():
    topic_counter = {tech.lower(): 0 for tech in TECHNOLOGIES}
    article_json = get_json_from_file()

    total = 0
    for row in article_json:
        if 'title' in row and 'time' in row:
            title = row['title']
            total += 1
            for word in title.lower().split():
                if word in map(str.lower, TECHNOLOGIES):
                    topic_counter[word] += 1
    probabilities =  {key: val / total for key, val in topic_counter.items()}
    print(probabilities)
    total_time = article_json[-1]['time']-article_json[0]['time']
    months_in_train_set = total_time/ SECONDS_IN_MONTH
    expected_posts_per_month = total/months_in_train_set
    print(expected_posts_per_month)
    #1 - peob^expected_posts_per_month


if __name__ == '__main__':
    learn_stuff()
    show_top()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
