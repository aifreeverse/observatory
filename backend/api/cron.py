
from .. import crud, schemas
from ..database import SessionLocal
from ..gutenberg_scraper import find_content_gaps_from_gutenberg

def handler(event, context):
    """The main function to be scheduled."""
    print("Starting data analysis cycle...")
    db = SessionLocal()

    all_gaps = []

    # Project Gutenberg Analysis
    gutenberg_urls = [
        "https://www.gutenberg.org/files/1342/1342-h/1342-h.htm", # Pride and Prejudice
        "https://www.gutenberg.org/files/11/11-h/11-h.htm", # Alice's Adventures in Wonderland
        "https://www.gutenberg.org/files/2701/2701-h/2701-h.htm", # Moby Dick
    ]
    gaps = find_content_gaps_from_gutenberg(gutenberg_urls)
    all_gaps.extend(gaps)

    # Clear existing gaps and store new ones
    db.query(schemas.ContentGap).delete()
    for gap_data in all_gaps:
        gap = schemas.ContentGapCreate(**gap_data)
        crud.create_content_gap(db, gap)

    print("Data analysis cycle complete.")
    db.close()

    return {
        'statusCode': 200,
        'body': 'Data analysis cycle complete.'
    }
