import streamlit as st
import tweepy
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import numpy as np
import string
import re
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns

consumerKey = # enter your own
consumerSecret = # enter your own
accessToken = # enter your own
accessTokenSecret = # enter your own

authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret) 
    
authenticate.set_access_token(accessToken, accessTokenSecret) 
    
api = tweepy.API(authenticate, wait_on_rate_limit = True)

def app():
	st.title("Tweet Analyzer 🔥")
	activities=["Select A Hashtag","Select A User"]
	choice = st.sidebar.selectbox("Select Your Activity",activities)

	if choice=="Select A Hashtag":
		st.subheader("Analyze the tweets of the hashtag you are interested in!")
		st.subheader("This tool performs the following tasks :")
		st.write("1. Fetches the 5 most recent tweets containing the hashtag")
		st.write("2. Generates a Word Cloud")
		st.write("3. Performs Sentiment Analysis a displays it in a Bar Graph")
		raw_text = st.text_area("Enter the hashtag (without #)")

		Analyzer_choice = st.selectbox("Select the Activities",  ["Show Recent Tweets","Generate WordCloud" ,"Visualize the Sentiment Analysis"])
		if st.button("Analyze"):	
			if Analyzer_choice == "Show Recent Tweets":
				st.success("Fetching last 5 Tweets...")
				def search_for_hashtags(hashtag_phrase):
					df = pd.DataFrame(columns = ['timestamp', 'tweet_text', 'username', 'all_hashtags', 'followers_count'])
					for tweet in tweepy.Cursor(api.search_tweets, q=hashtag_phrase+' -filter:retweets', lang="en", tweet_mode='extended').items(30):
						df = df.append({'timestamp': tweet.created_at, 'tweet_text': tweet.full_text.replace('\n',' ').encode('utf-8'), 'username': tweet.user.screen_name.encode('utf-8'), 'all_hashtags': [e['text'] for e in tweet._json['entities']['hashtags']], 'followers_count': tweet.user.followers_count}, ignore_index = True)
					def get_tweets(df):
						l=[]
						i=1
						for tweet in df['tweet_text'][:5]:
							l.append(tweet)
							i= i+1
						return l
					recent_tweets=get_tweets(df)		
					return recent_tweets
				recent_tweets= search_for_hashtags(raw_text)
				st.write(recent_tweets)


			elif Analyzer_choice=="Generate WordCloud":
				st.success("Generating Word Cloud...")
				hashtag_phrase = raw_text
				df = pd.DataFrame(columns = ['tweet_text', 'all_hashtags'])
				for tweet in tweepy.Cursor(api.search_tweets, q=hashtag_phrase+' -filter:retweets', lang="en", tweet_mode='extended').items(30):
					df = df.append({'tweet_text': tweet.full_text.replace('\n',' ').encode('utf-8'), 'all_hashtags': [e['text'] for e in tweet._json['entities']['hashtags']]}, ignore_index = True)
					
				punc = '''[]'",'''
				df['hashtag_list'] = ''
				input_str = df['all_hashtags']
				for i in range(0, len(df)):
					s = input_str[i]
					for ele in s:
						if ele in punc:
							s = s.replace(ele, "")
					df['hashtag_list'][i] =  s

				flat_hashtag = []
				for hlist in df['hashtag_list']:
					for h in hlist:
						h = h.upper()
						flat_hashtag.append(h)

				s = hashtag_phrase[1:].upper()
				stop_words = STOPWORDS.update([s])

				wordcloud = WordCloud(width=500, 
					height=300,
					max_font_size=50,
                    stopwords = stop_words,
                    collocations=False,
                    background_color ='black',
                    colormap='twilight_shifted'
                    #,font_path='SourceHanSans.ttc'
					).generate(" ".join(flat_hashtag))
				# plt.figure(figsize = (40, 40), facecolor = None)
				plt.imshow(wordcloud)
				plt.axis("off")
				plt.tight_layout(pad = 0)
				plt.savefig("wc.png", format="png")	
				img= Image.open("WC.png") 
				st.image(img)

			else:
				st.success("Generating Visualisation for Sentiment Analysis...")
				words = [w for w in nltk.corpus.state_union.words() if w.isalpha()]
				stopwords = nltk.corpus.stopwords.words("english")

				hashtag_phrase = raw_text
				df = pd.DataFrame(columns = ['tweet_text', 'all_hashtags'])
				for tweet in tweepy.Cursor(api.search_tweets, q=hashtag_phrase+' -filter:retweets', lang="en", tweet_mode='extended').items(30):
					df = df.append({'tweet_text': tweet.full_text.replace('\n',' ').encode('utf-8'), 'all_hashtags': [e['text'] for e in tweet._json['entities']['hashtags']]}, ignore_index = True)
	
				for i in range(len(df)):
					df['tweet_text'][i] = df['tweet_text'][i][2:]
				english_punctuations = string.punctuation
				punctuations_list = english_punctuations
				def cleaning(data):
					data = re.sub(b"((www.[^s]+)|(https?://[^s]+))",b"",data)
					data = re.sub(b"\@\w+[,]|\@\w+|[,]\@\w+", b"", data)
					#data = re.sub(b"\\x\w+[,]|\\x\w+|[,]\\x\w+", b"", data)
					data = re.sub(b"\#\w+[,]|\#\w+|[,]\#\w+", b"", data)
					data = re.sub(b'[0-9]+', b'', data)
					#translator = str.maketrans('', '', punctuations_list)
					#data = data.translate(translator)
					return re.sub(b'[^a-zA-Z]',b' ',data)
				flat_tweets = df['tweet_text'].apply(lambda x: cleaning(x))
				stopwords = nltk.corpus.stopwords.words("english")
				def cleaning_stopwords(text):
					return " ".join([word for word in str(text).split() if word not in stopwords])
				flat_tweets = flat_tweets.apply(lambda text: cleaning_stopwords(text))
				data = flat_tweets.to_frame(name='text')

				sid = SentimentIntensityAnalyzer()
				data['vader_Polarity'] = data['text'].apply(sid.polarity_scores)
				data['vader_res']  = data['vader_Polarity'].apply(lambda score_dict: score_dict['compound'])
				data['vader_Analysis'] = data['vader_res'].apply(lambda c: 'Positive' if c >=0 else 'Negative')

				st.write(sns.countplot(x=data['vader_Analysis'], data=data))
				st.pyplot(use_container_width=True)
	else:
		st.subheader("More functions coming up!")



if __name__ == "__main__":
	app()