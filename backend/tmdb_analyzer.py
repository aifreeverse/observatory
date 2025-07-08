
import tmdbsimple as tmdb
import os
from dotenv import load_dotenv
from collections import Counter
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

load_dotenv()

# --- TMDB API Configuration ---
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
tmdb.API_KEY = TMDB_API_KEY

def get_tmdb_data(query: str, limit: int = 20):
    """Fetches movie/TV show data from TMDB based on a query."""
    if not TMDB_API_KEY:
        print("TMDB API key not found. Skipping TMDB analysis.")
        return []

    search = tmdb.Search()
    response = search.movie(query=query)

    all_overviews = ""
    for movie in response['results']:
        if movie.get('overview'):
            all_overviews += movie['overview'] + " "
        if limit and len(all_overviews.split()) > 1000: # Limit text to avoid excessive processing
            break

    return all_overviews

def analyze_text_tmdb(text: str):
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
            gaps.append({"title": title, "demand_score": demand_score, "sources": "tmdb"})

        for plot, plot_count in Counter(found_plots).most_common(3):
            title = f"{genre} with a {plot} plot"
            demand_score = round((genre_count + plot_count) / 2, 2)
            gaps.append({"title": title, "demand_score": demand_score, "sources": "tmdb"})

        for setting, setting_count in Counter(found_settings).most_common(3):
            title = f"{genre} set in a {setting}"
            demand_score = round((genre_count + setting_count) / 2, 2)
            gaps.append({"title": title, "demand_score": demand_score, "sources": "tmdb"})

    return gaps

def find_content_gaps_from_tmdb(query: str):
    """Orchestrates the process of finding content gaps from TMDB."""
    print(f"Analyzing TMDB for query: {query}...")
    text = get_tmdb_data(query)
    if not text:
        return []

    gaps = analyze_text_tmdb(text)
    return gaps
