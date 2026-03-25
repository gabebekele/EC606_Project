import pandas as pd
from tree import AVLTree

def build_tree(fname):
    """
    Load Reddit submissions CSV and build an AVL tree indexed by score.
    Stores unixtime internally for easy filtering.
    """
    df = pd.read_csv(fname, engine="python", on_bad_lines="skip")

    # Drop rows with missing critical info
    df = df.dropna(subset=['score', 'title', 'username', 'rawtime'])
    df = df.drop_duplicates(subset=['reddit_id'])

    # Convert rawtime to UTC-aware datetime
    df['time_posted'] = pd.to_datetime(df['rawtime'], errors='coerce', utc=True)

    # Convert to unixtime for internal storage
    df['unixtime'] = df['time_posted'].apply(lambda x: int(x.timestamp()) if pd.notnull(x) else None)

    # Optional: add convenience columns
    df['year'] = df['time_posted'].dt.year
    df['month'] = df['time_posted'].dt.month
    df['day'] = df['time_posted'].dt.day
    df['hour'] = df['time_posted'].dt.hour
    df['weekday'] = df['time_posted'].dt.day_name()

    tree = AVLTree()

    # Build AVL tree
    for _, row in df.iterrows():
        post_data = {
            "subreddit": row["subreddit"],
            "title": row["title"],
            "id": row["username"],
            "unixtime": row["unixtime"],  # internal timestamp
            "score": row["score"]
        }
        tree.add(row["score"], post_data)

    return tree, df
