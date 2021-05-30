# Kovrr Assignment

This project can do 3 nice things related to Hacker News:
1. Show current top 40 articles
2. Calculate likelihood of topics appearing next month
3. (Bonus) Show correlation between proximity of posting time to 8pm and the number of comments on the article

## Installation

Verified for python 3.7 with the packages listed in the requirements.txt file

```bash
 pip install -r requirements.txt 
```

## Example usage

```python
python main.py --top-stories
```

## Command line options
Choose 1 Hacker News related action


#### options:
####  -t, --top-stories
Show the titles of the top 40 articles right now

####  -l, --tech-likelihood
 
You will be given a choice of technology, its' likelihood of appearance the following month will be shown

####  -c, --comment-correlation
(Bonus)
Find correlation between post hour and number of comments

