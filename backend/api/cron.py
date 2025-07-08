
from .. import crud, schemas
from ..database import SessionLocal
from ..reddit_analyzer import find_content_gaps_from_reddit

def handler(event, context):
    """The main function to be scheduled."""
    print("Starting data analysis cycle...")
    db = SessionLocal()

    # For now, we'll analyze a few relevant subreddits
    subreddits = ["movies", "television", "books"]
    all_gaps = []
    for sub in subreddits:
        gaps = find_content_gaps_from_reddit(sub)
        all_gaps.extend(gaps)

    # Clear existing gaps and store new ones
    # A more sophisticated approach would be to update existing gaps
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
