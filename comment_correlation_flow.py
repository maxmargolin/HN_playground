import datetime

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import utils
from utils import get_json_from_file


def article_time_correlation():
    """
    Full flow of time of day to number of comments correlation
    """
    articles = get_json_from_file()
    data_samples = articles_to_filtered_df(articles)
    report_correlation_result(data_samples)


def articles_to_filtered_df(articles):
    """
    turn list of articles into df with relevant columns
    """
    data_samples = []
    est_offset_below_utc = datetime.timedelta(hours=5)

    for article in articles:
        if 'time' in article and 'descendants' in article:
            post_time = article['time']
            # Transform unix utc to est, 1 AM UTC i 8pm EST
            post_est_time = datetime.datetime.utcfromtimestamp(post_time) - est_offset_below_utc

            # Find proximity of this time to 8PM, Ignoring seconds
            minutes_of_day_est = post_est_time.hour * 60 + post_est_time.minute
            delta_from_8pm = abs(utils.COMPARISON_POINT - minutes_of_day_est)
            data_samples.append([delta_from_8pm, article['descendants']])

    return data_samples


def report_correlation_result(data_samples):
    """
    Show correlation graph
    """
    column_names = ['distance_from_8pm', 'comments_amount']
    df = pd.DataFrame(data_samples, columns=column_names)

    # show matrix
    corr = df.corr()
    fig = plt.figure()
    ax = fig.add_subplot(111)  # necessary
    cax = ax.matshow(corr, interpolation='nearest')
    fig.colorbar(cax)
    axis = np.arange(len(column_names))
    ax.set_xticks(axis)
    ax.set_yticks(axis)
    ax.set_xticklabels(column_names)
    ax.set_yticklabels(column_names)

    # report correlation
    corr_value = corr.iat[0, 1]
    plt.title(f"Correlation:{corr_value}")
    print(f"Correlation between Distance to 8pm and #comments: {corr_value}")  # so no correlation for sample file
    plt.show()
