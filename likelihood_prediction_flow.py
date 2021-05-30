import logging

from matplotlib import pyplot as plt
from scipy.stats import binom

import config
from utils import get_json_from_file, SECONDS_IN_MONTH


def prompt_tech_selection(technologies=config.TECHNOLOGIES):
    """
    Ask user to select a technology from the list, return selection
    """
    print("Select technology number for probability analysis from:")
    for i, tech in enumerate(technologies):
        print(f"{i + 1}. {tech}")
    print("Insert technology number for probability analysis:")

    user_input = input()
    if not user_input.isdigit() or int(user_input) > len(technologies) or int(user_input) < 1:
        selection = 1
        logging.warning(f"Bad input, using default selection {selection}")
    else:
        selection = int(user_input)
    return technologies[selection - 1]


def likelihood_prediction():
    """
    Full flow of asking user to choose a technology and displaying its' likelihood to appear
    """
    # Get info
    selected_word = prompt_tech_selection()
    article_json = get_json_from_file()

    # Calculate results
    total_word_counter, selected_word_counter = count_occurrences(article_json, selected_word)
    probability = selected_word_counter / total_word_counter
    total_time = article_json[-1]['time'] - article_json[0]['time']  # unix subtraction = seconds
    months_in_train_set = total_time / SECONDS_IN_MONTH
    expected_posts_per_month = int(total_word_counter / months_in_train_set)

    # Show results
    print_text_results(expected_posts_per_month, probability, selected_word)
    plot_likelihood(expected_posts_per_month, probability)


def print_text_results(total_monthly_articles, probability, selected_word):
    """
    Print the text part of the likelihood calculation result
    """
    print(f"Probability of word {selected_word} per title: {probability}")
    print(f"Expecting {total_monthly_articles} overall HN posts per month")
    prob_at_least_once = 1 - (1 - probability) ** total_monthly_articles
    print(f"Probability of ~{prob_at_least_once} for '{selected_word}' to appear at least once next month ")


def count_occurrences(article_json, selected_word):
    """
    Count occurrences of a specific word in the titles of a list of articles
    """
    selected_word = selected_word.lower()
    total_titles = 0  # some rows miss the title field, so not using len()
    selected_word_counter = 0
    for row in article_json:
        if 'title' in row:
            title = row['title']
            total_titles += 1
            for word_in_title in title.lower().split():
                if word_in_title == selected_word:
                    selected_word_counter += 1
    return total_titles, selected_word_counter


def plot_likelihood(expected_posts_per_month, probability):
    """
    Show a graph of the likelihood for number of occurrences
    """
    bar_amount = max(10, int(5 * expected_posts_per_month * probability))  # at least 10 bars, not too long of a tail
    print("Generating likelihood plot")
    distribution = [binom.pmf(option, expected_posts_per_month, probability) for option in range(bar_amount)]
    plt.bar(range(bar_amount), distribution)
    plt.xlabel("occurrences")
    plt.ylabel("likelihood")
    plt.title("Likelihood of word occurences next month")
    plt.show()
