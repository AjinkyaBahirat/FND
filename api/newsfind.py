from newsapi import NewsApiClient

# create a newsapi client
newsapi = NewsApiClient(api_key='0bafa3367a2d4d6286889bce3bd16e61')

# specify the search keyword
keyword = "Cops In Pursuit"

# fetch news articles related to the keyword
articles = newsapi.get_everything(q=keyword)

# print the titles of the articles
for article in articles['articles']:
    print(article['title'])
