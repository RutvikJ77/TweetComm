import streamlit as st
from processing import fetch_comments, matplot
from Tweet_embedded import Tweet

st.title("👥Tweetcom")

clicked = False
row1_1, row1_2 = st.columns((3,2))

def clicked_func(clicked = False):
    if clicked:
        with row1_1:
            tweet_data = fetch_comments(tweet_url)
            st.pyplot(matplot(tweet_data['Tweets']))


with row1_1:
    tweet_url = st.text_input("Enter the tweet url for analysis:")
    
    
with row1_2:
    if st.button("Fetch"):
        tweet_obj = Tweet(tweet_url).component()
        clicked = True
        clicked_func(clicked)
