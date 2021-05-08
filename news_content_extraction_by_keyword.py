
"""Basic uses of this module:
    1) To generate a csv of title and text from news articles based on search
       <search>, use generate_data_frame(search).
    2) To generate a csv with name <name> of title and text from news articles
       given that their urls are saved in a txt file with path <path>,
       use generate_df_from_txt(path, name).
"""

from googlesearch import search # news url extracting API: https://python-googlesearch.readthedocs.io/en/latest/ , https://python-googlesearch.readthedocs.io/en/latest/_modules/googlesearch.html command: pip install google
from newspaper import Article # newspaper API: https://buildmedia.readthedocs.org/media/pdf/newspaper/latest/newspaper.pdf command: pip install newspaper3k
from newsplease import NewsPlease # news-please API: https://github.com/fhamborg/news-please command: pip install news-please
import os
import re
import pandas as pd
from typing import List, Tuple
from langdetect import detect


def search_keyword(keywords, idx):
    """Return the <idx> url for a Google News search on <keywords>."""

    # search returns an iterator of urls
    # tbs is the time to search (“qdr:d” is last day, “qdr:m” is last month)
    for url in search(keywords, lang="en", tbs="qdr:w", pause = 0.1, start = idx, stop = idx + 1):
        # search the url, if video does not appear in it then return it
        pattern_skip = 'video'
        if not re.search(pattern_skip, url):
            return url
    return None

def process_news_paper(url: str) -> Tuple[str, str]:
    """Use the newspaper API to get the article content."""
    article = Article(url)
    article.download()
    article.parse()
#    # Throw exception if text is too short
#    if len(article.text.split()) < 50:
#        raise Exception
    # Throw exception if text or title is only whitespace
    if article.title.strip() == '' or article.text.strip() == '':
        raise Exception
    # Throw exception if title or text is not english.
    if detect(article.text) != 'en' or detect(article.title) != 'en':
        raise Exception
    return article.title, article.text

def process_news_please(url: str) -> Tuple[str, str]:
    """Use the news-please API to get the article content."""
    article = NewsPlease.from_url(url)
    # Throw exception if text or title is only whitespace
    if article.title.strip() == '' or article.text.strip() == '':
        raise Exception
    # Throw exception if title or text is not english.
    if detect(article.text) != 'en' or detect(article.title) != 'en':
        raise Exception
    return article.title, article.text

def extract_info_from_url(url: str) -> Tuple[str, str]:
    """Return the title and text of article url."""

    # Try newspaper API first, if it fails, use news-please API
    try:
        result = process_news_paper(url)
        #print(url + "\n scraped by newspaper API.")
    except:
        try:
            result = process_news_please(url)
            #print(url + "\n scraped by news-please API.")
        except:
            #print(url + "\n cannot be scraped by either API.")
            result = '', ''

    return result


def summarize_article_search(keywords, limit = 1000):
    for i in range(limit):
        url = search_keyword(keywords, i)
        if url is None:
            continue
        title, text = extract_info_from_url(url)
        if title == '' or text == '':
            continue

        # Use Open.ai here
        result = title + " is an article related to the search " + keywords + "\n"
        result += "This article is about: \n" + text[:1000] + "\n"
        result += "To read more, see " + url
        return result

if __name__ == "__main__":
    print(summarize_article_search("covid"))
