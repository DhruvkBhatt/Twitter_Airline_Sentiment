"""
Sentiment Analysis of Tweets about US Airlines
------------------------------------------------
This Streamlit application loads a CSV of airline‐related tweets,
performs basic sentiment analysis counts and visualizations, and
lets users explore the data interactively:

• Random tweet display by sentiment  
• Sentiment‐count histogram or pie chart  
• Mapping tweets by hour of day  
• Faceted bar charts breaking down airlines by sentiment  
• Word clouds for positive, negative or neutral tweets  

Usage:
    $ streamlit run app.py

Author: Dhruv Bhatt
Date:   2025-07-05
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets about US Airlines")

st.markdown(" This application is a Streamlit app used to analyze the sentiment of the tweets 🐦 about US airlines ✈️ ")
st.sidebar.markdown(" This application is a Streamlit app used to analyze the sentiment of the tweets 🐦 about US airlines ✈️ ")


DATA_URL = ("Tweets.csv")

@st.cache_data(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()

st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio('Sentiment type', ('positive','negative','neutral'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])

st.sidebar.markdown("### Number of tweets by sentiment type")
select = st.sidebar.selectbox('Vizualization type', ['Histogram', 'Pie Chart'], key='1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment' :sentiment_count.index, 'Tweets' :sentiment_count.values})

if not st.sidebar.checkbox('Hide'):
    st.markdown("### Number of tweets by Sentiment")
    if select == "Histogram":
        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color = 'Tweets', height= 500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)

st.sidebar.subheader("When and where are the users tweeting from?")
hour = st.sidebar.slider("Hour of day", 0, 23)
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox("Close", True, key='2'):
    st.markdown("### Tweets location based on the time of the day")
    st.markdown("%i, tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)


st.sidebar.subheader("Breakdown airline tweets by sentiment")
choice = st.sidebar.multiselect("Pick airlines", ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'), key = '0')


if len(choice) >0:
    choice_data = data[data.airline.isin(choice)]
    fig_0 = px.histogram(choice_data, x='airline', y='airline_sentiment', histfunc='count', color='airline_sentiment', facet_col = 'airline_sentiment', labels={'airline_sentiment':'tweets'}, height=600, width=800)
    st.plotly_chart(fig_0)

st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Display word cloud for which sentiment?', ('positive', 'negative', 'neutral'))

if not st.sidebar.checkbox("Close", True, key='3'):
    # st.header(f'Word cloud for {word_sentiment} sentiment')
    df = data[data['airline_sentiment'] == word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join(
        w for w in words.split()
        if not w.startswith('http') and not w.startswith('@') and w != 'RT'
    )

    # Create a figure & axes
    fig, ax = plt.subplots(figsize=(8, 6))
    wordcloud = WordCloud(
        stopwords=STOPWORDS,
        background_color='white',
        height=600,
        width=800
    ).generate(processed_words)

    # Draw on that axes
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')  # remove the axes ticks
    ax.set_title(f'Word Cloud for {word_sentiment} Sentiment', fontsize=20)
    # Adjust layout to prevent clipping of titles
    plt.tight_layout()

    # Pass the figure into st.pyplot
    st.pyplot(fig)
