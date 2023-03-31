import requests
import base64
import json
import tweepy
import openai
import random
import time

client = tweepy.Client(bearer_token='')

# Twitter API keys and access tokens
consumer_key = ''
consumer_secret = ""
access_token = ""
access_token_secret = ""

# Authenticate to Twitter API
'''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
'''
# Create API object
client = tweepy.Client(consumer_key=consumer_key,
                       consumer_secret=consumer_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret)

# OpenAI API key
openai.api_key = ""

# DALL-E API endpoint and API key
dalle_api_endpoint = "https://api.openai.com/v1/images/generations"
dalle_api_key = openai.api_key

# LOTR quotes
lotr_quotes = [
    "All we have to decide is what to do with the time that is given us. - Gandalf",
    "Even the smallest person can change the course of history. - Galadriel",
    "I would rather share one lifetime with you than face all the ages of this world alone. - Arwen",
    "It is not despair, for despair is only for those who see the end beyond all doubt. We do not. - Gandalf",
    "The board is set, the pieces are moving. We come to it at last, the great battle of our time. - Gandalf"
]

# Function to generate ChatGPT commentary
def generate_commentary(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

# Function to generate DALL-E image
def generate_image(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {dalle_api_key}"
    }
    data = {
        "model": "image-alpha-001",
        "prompt": prompt,
        "num_images": 1,
        "size": "512x512",
        "response_format": "url"
    }
    response = requests.post(dalle_api_endpoint, headers=headers, json=data)
    response.raise_for_status()
    response_data = response.json()
    return response_data["data"][0]["url"]

# Main loop to tweet once a day
while True:
    # Generate random quote
    prompt_1 = 'What is a random quote from LOTR or the Silmarillion that is not very well-known?'
    quote = generate_commentary(prompt_1)
    # Generate commentary
    prompt = f"What does \"{quote}\" mean in the context of LOTR?"
    commentary = generate_commentary(prompt)
    # Generate image
    #image_prompt = f"\"{quote}\" in LOTR"
    #image_url = generate_image(image_prompt)
    # Download image
    #response = requests.get(image_url)
    # Save image to file
    #with open("/Users/anthonyklemm/Documents/Data630_Datasets/Twitter/image.png", "wb") as f:
        #f.write(response.content)
    # Upload image to Twitter
    #media = api.media_upload(filename="image.png")
    # Tweet the quote, commentary, and image
    tweet = f"{quote}\n\n{commentary}\n\n{'#LOTR #LOTRROP'}"
    tweet = tweet[:280]
    response = client.create_tweet(text=tweet)
    # Wait 12 hours before tweeting again
    time.sleep(60*60)
