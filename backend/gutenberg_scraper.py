
import requests
from bs4 import BeautifulSoup
import spacy
from collections import Counter

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def get_gutenberg_text(url: str, limit_chars: int = 5000):
    """Fetches text from a Project Gutenberg book URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the main content of the book (this might need adjustment for different book formats)
        # A common pattern is to look for <pre> tags or specific div IDs
        text_content = ""
        for tag in soup.find_all('pre'):
            text_content += tag.get_text()
        if not text_content:
            # Fallback for other structures, e.g., plain text within body or specific divs
            text_content = soup.body.get_text()

        return text_content[:limit_chars] # Return a limited portion of the text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return ""

def analyze_text_gutenberg(text: str):
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
    gaps = []
    for genre, genre_count in Counter(found_genres).most_common(3):
        for archetype, archetype_count in Counter(found_archetypes).most_common(3):
            title = f"{genre} with a {archetype}"
            demand_score = round((genre_count + archetype_count) / 2, 2)
            gaps.append({"title": title, "demand_score": demand_score, "sources": "gutenberg"})

        for plot, plot_count in Counter(found_plots).most_common(3):
            title = f"{genre} with a {plot} plot"
            demand_score = round((genre_count + plot_count) / 2, 2)
            gaps.append({"title": title, "demand_score": demand_score, "sources": "gutenberg"})

        for setting, setting_count in Counter(found_settings).most_common(3):
            title = f"{genre} set in a {setting}"
            demand_score = round((genre_count + setting_count) / 2, 2)
            gaps.append({"title": title, "demand_score": demand_score, "sources": "gutenberg"})

    return gaps

def find_content_gaps_from_gutenberg(urls: list[str]):
    """Orchestrates the process of finding content gaps from Project Gutenberg."""
    all_text = ""
    for url in urls:
        print(f"Fetching from Project Gutenberg: {url}...")
        all_text += get_gutenberg_text(url)

    if not all_text:
        return []

    gaps = analyze_text_gutenberg(all_text)
    return gaps
