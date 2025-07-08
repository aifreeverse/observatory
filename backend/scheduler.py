
from apscheduler.schedulers.background import BackgroundScheduler
from . import crud, schemas
from .database import SessionLocal, ContentGap as ContentGapModel
from .reddit_analyzer import find_content_gaps_from_reddit

def analyze_and_store_data():
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
    db.query(ContentGapModel).delete()
    for gap_data in all_gaps:
        gap = schemas.ContentGapCreate(**gap_data)
        crud.create_content_gap(db, gap)

    print("Data analysis cycle complete.")
    db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(analyze_and_store_data, 'interval', hours=1)
