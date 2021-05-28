import json
from functools import partial
from multiprocessing.pool import ThreadPool

import matplotlib.pyplot as plt
import numpy as np
import requests
from scipy.stats import binom

import config
from utils import SECONDS_IN_MONTH, list_to_chunks, get_json_from_file


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


def prompt_tech_selection(technologies=config.TECHNOLOGIES):
    print("Select technology number for probability analysis from:")
    for i, tech in enumerate(technologies):
        print(f"{i + 1}. {tech}")
    print("insert technology number for probability analysis:")

    user_input = input()
    if not user_input.isdigit() or int(user_input) > len(technologies) or int(user_input) < 1:
        selection = 1
        print(f"Using default selection {selection}")
    selection = int(user_input)
    return technologies[selection - 1]


def likelihood_prediction():
    selected_word = prompt_tech_selection()
    article_json = get_json_from_file()

    total, word_counter = count_occurrences(article_json, selected_word)
    probability = word_counter / total
    total_time = article_json[-1]['time'] - article_json[0]['time']
    months_in_train_set = total_time / SECONDS_IN_MONTH
    expected_posts_per_month = int(total / months_in_train_set)

    print_text_results(expected_posts_per_month, probability, selected_word)
    plot_likelihood(expected_posts_per_month, probability)


def print_text_results(monthly_cmount, probability, selected_word):

    print(f"probability of word {selected_word} per title: {probability}")
    print(f"expecting {monthly_cmount} posts per month")
    prob_atleast_once = 1 - (1 - probability) ** (monthly_cmount)
    print(f"probability of ~{prob_atleast_once} for '{selected_word}' to appear at least once next month ")


def count_occurrences(article_json, selected_word):
    selected_word = selected_word.lower()
    total = 0
    word_counter = 0
    for row in article_json:
        if 'title' in row and 'time' in row:
            title = row['title']
            total += 1
            for word_in_title in title.lower().split():
                if word_in_title == selected_word:
                    word_counter += 1
    return total, word_counter


def plot_likelihood(expected_posts_per_month, probability):
    columns = max(10, int(5 * expected_posts_per_month * probability))
    print("generating plot")
    dist = [binom.pmf(r, expected_posts_per_month, probability) for r in range(columns)]
    plt.bar(range(columns), dist)
    plt.xlabel("occurrences")
    plt.ylabel("likelihood")
    plt.show()


if __name__ == '__main__':
    likelihood_prediction()
    # show_top()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
