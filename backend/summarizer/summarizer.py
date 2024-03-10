import requests
from newsapi import NewsApiClient
from transformers import pipeline

# Initialize the NewsAPI client
newsapi = NewsApiClient(api_key='0060309c3ac44f6daa0245c75b842ba0')

# Initialize the summarization pipeline
summarizer = pipeline('summarization')

# List of news sources
sources = ['wall-street-journal', 'cnn', 'cnbc', 'fox-news', 'bbc-news']

def get_news_summaries():
    news_summaries = []
    for source in sources:
        articles = newsapi.get_top_headlines(sources=source, language='en')['articles']

        for article in articles[:10]:
            article_summary = {
                'title': article['title'],
                'link': article['url'],
                'author': article['author'] if article['author'] else 'Unknown',
                'bulletPoints': []
            }

            if 'content' in article and article['content']:
                try:
                    summary = summarizer(article['content'], max_length=200, min_length=30, do_sample=False)[0]['summary_text']
                    bullet_points = [f"- {point.strip()}" for point in summary.split('.') if point.strip()]
                    bullet_points = bullet_points[:5]  # Take the first 5 bullet points
                    article_summary['bulletPoints'] = bullet_points
                except (KeyError, IndexError):
                    article_summary['bulletPoints'] = ["- Unable to generate key points for this article."]
            else:
                article_summary['bulletPoints'] = ["- Article content not available."]

            news_summaries.append(article_summary)

    return news_summaries