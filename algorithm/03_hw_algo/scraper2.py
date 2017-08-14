import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

response = requests.get("http://www.sueddeutsche.de")
doc = BeautifulSoup(response.text, 'html.parser')

stories = doc.find_all("div", {'class': 'teaser top nooverline'})

all_stories = []
# Grab their headlines and bylines
for story in stories:
    # Grab all of the h2's inside of the story
    headline = story.find('a', {'class': 'entry-title'})
    # If a headline exists, then process the rest!
    if headline:
        # They're COVERED in whitespace
        headline_text = headline.text.strip()
        # Make a dictionary with the headline
        this_story = { 'headline': headline_text }
        byline = story.find('span', {'class': 'author'})
        # Not all of them have a byline
        if byline:
            byline_text = byline.text.strip()
            this_story['byline'] = byline_text
        all_stories.append(this_story)

print(all_stories)

stories_df = pd.DataFrame(all_stories)
stories_df.to_csv("sz.csv")

datestring = time.strftime("%Y-%m-%d-%H-%M")

filename = "sz-" + datestring + ".csv"
stories_df.to_csv(filename, index=False)