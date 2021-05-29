import argparse
import logging

from comment_correlation_flow import article_time_correlation
from likelihood_prediction_flow import likelihood_prediction
from top_article_flow import show_top


def main():
    parser = argparse.ArgumentParser(description="Choose 1 Hacker News related action")
    parser.add_argument('-t', '--top-stories', action='store_true',
                        help="Show the titles of the top 40 articles right now")
    parser.add_argument('-l', '--tech-likelihood', action='store_true',
                        help="You will be given a choice of technology,"
                             "it's likelihood of appearance the following month will be shown")
    parser.add_argument('-c', '--comment-correlation', action='store_true',
                        help="Find correlation between post hour and number of comments")
    args = parser.parse_args()
    if args.top_stories:
        show_top()
    elif args.tech_likelihood:
        likelihood_prediction()
    elif args.comment_correlation:
        article_time_correlation()
    else:
        logging.error("No action chosen")
        parser.print_help()


if __name__ == '__main__':
    main()
