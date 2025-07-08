
import praw
import spacy
from collections import Counter
from dotenv import load_dotenv
import os

load_dotenv()

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# --- Reddit API Configuration ---
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
)

def get_reddit_data(subreddit_name: str, limit: int = 100):
    """Fetches and analyzes data from a given subreddit."""
    if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT]):
        print("Reddit API credentials not found. Skipping Reddit analysis.")
        return ""

    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
    )

    subreddit = reddit.subreddit(subreddit_name)
    hot_posts = subreddit.hot(limit=limit)

    all_text = ""
    for post in hot_posts:
        all_text += post.title + " "
        post.comments.replace_more(limit=0) # Remove "load more comments" links
        for comment in post.comments.list():
            all_text += comment.body + " "

    return all_text

def analyze_text(text: str):
    """Analyzes text to find common noun phrases and identify narrative elements."""
    from .taxonomies import CHARACTER_ARCHETYPES, PLOT_STRUCTURES, SETTING_ELEMENTS, GENRES

    doc = nlp(text.lower()) # Convert to lowercase for better matching

    # Identify genres
    found_genres = []
    for genre, keywords in GENRES.items():
        if any(keyword in text for keyword in keywords):
            found_genres.append(genre)

    # Identify archetypes
    found_archetypes = []
    for archetype, keywords in CHARACTER_ARCHETYPES.items():
        if any(keyword in text for keyword in keywords):
            found_archetypes.append(archetype)

    # Identify plot structures
    found_plots = []
    for plot, keywords in PLOT_STRUCTURES.items():
        if any(keyword in text for keyword in keywords):
            found_plots.append(plot)

    # Identify setting elements
    found_settings = []
    for setting, keywords in SETTING_ELEMENTS.items():
        if any(keyword in text for keyword in keywords):
            found_settings.append(setting)

    # Combine the findings into a structured result
    # This is a simplified combination logic. A more advanced system could find more nuanced connections.
    # For now, we'll create gaps from the most common combinations.

    # Count the frequency of each element
    genre_counts = Counter(found_genres)
    archetype_counts = Counter(found_archetypes)
    plot_counts = Counter(found_plots)
    setting_counts = Counter(found_settings)

    # Generate content gaps based on the most common combinations
    # This is still a simplification. A real system would need more sophisticated analysis
    # to determine which combinations are truly in demand.
    gaps = []
    for genre, genre_count in genre_counts.most_common(3):
        for archetype, archetype_count in archetype_counts.most_common(3):
            title = f"{genre} with a {archetype}"
            demand_score = round((genre_count + archetype_count) / 2, 2)
            gaps.append({"title": title, "demand_score": demand_score, "sources": "reddit"})

        for plot, plot_count in plot_counts.most_common(3):
            title = f"{genre} with a {plot} plot"
            demand_score = round((genre_count + plot_count) / 2, 2)
            gaps.append({"title": title, "demand_score": demand_score, "sources": "reddit"})

        for setting, setting_count in setting_counts.most_common(3):
            title = f"{genre} set in a {setting}"
            demand_score = round((genre_count + setting_count) / 2, 2)
            gaps.append({"title": title, "demand_score": demand_score, "sources": "reddit"})

    return gaps

def find_content_gaps_from_reddit(subreddit_name: str):
    """Orchestrates the process of finding content gaps from Reddit."""
    print(f"Analyzing subreddit: {subreddit_name}...")
    text = get_reddit_data(subreddit_name)
    if not text:
        return []

    gaps = analyze_text(text)
    return gaps
