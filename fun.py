import requests
from textblob import TextBlob
from dotenv import load_dotenv
import os 
import matplotlib.pyplot as plt



load_dotenv() #load environment variables from .env file

api_key=os.getenv("AIzaSyCL79TDlnpSaUvF4b59KKdQuQynmi-ofwc")




def fetch_comments(video_id):
    """Fetch comments from a YouTube video."""
    comments = []
    url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={API_KEY}&maxResults=100"
    
    while url:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for item in data["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment)
            # Handle pagination
            next_page_token = data.get("nextPageToken")
            if next_page_token:
                url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={API_KEY}&maxResults=100&pageToken={next_page_token}"
            else:
                break
        else:
            print(f"Error: {response.status_code}, {response.text}")
            break
    return comments

def analyze_sentiment(comments):
    """Analyze the sentiment of comments."""
    positive, negative, neutral = 0, 0, 0

    for comment in comments:
        analysis = TextBlob(comment)
        if analysis.sentiment.polarity > 0:
            positive += 1
        elif analysis.sentiment.polarity < 0:
            negative += 1
        else:
            neutral += 1

    return positive, negative, neutral

def plot_sentiment(positive, negative, neutral):
    """Plot the sentiment analysis results."""
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [positive, negative, neutral]
    colors = ['#2ecc71', '#e74c3c', '#95a5a6']
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Sentiment Analysis of Comments')
    plt.show()

# Video ID
video_id = "dgrddA6vnPI"

comments = fetch_comments(video_id)
if comments:
    print(f"Fetched {len(comments)} comments!")
    positive, negative, neutral = analyze_sentiment(comments)
    print(f"Positive: {positive}, Negative: {negative}, Neutral: {neutral}")
    plot_sentiment(positive, negative, neutral)
else:
    print("No comments found or an error occurred.")
