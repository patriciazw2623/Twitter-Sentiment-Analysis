# Twitter Sentiment Analysis
A natural language processing project based on python. 

The jupyter notebook file demonstrates a demo using hashtag "jeno", name of a member of the South Korean boy group NCT and its fixed sub-unit NCT Dream. The two images are the histogram and wordcloud created with the code.

The project has three parts: data-scraping from twitter, some data analysis (histogram, wordcloud, etc.) and the sentiment analysis.

The python package "Tweepy" is used to scrape tweets that contains a given keyword. More info on the package can be found in the [official documentation](https://docs.tweepy.org/en/stable/). To use Tweepy, a Twitter developer account is needed. 

The python packages "nltk" and "textblob" are used for sentiment analysis. "nltk" categorizes tweets into three groups, positive, neutral and negative emotions, while "textblob" only offers two categories, positive and negative.
