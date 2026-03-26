import pandas as pd
from tree import AVLTree

def build_tree(fname, menuItem=None, start=None, end=None):
    import pandas as pd
    from tree import AVLTree

    df = pd.read_csv(fname, engine="python", on_bad_lines="skip")

    # Clean dataset
    df = df.dropna(subset=['score', 'title', 'username', 'unixtime'])
    df = df.drop_duplicates(subset=['reddit_id'])

    # fix date format
    if start:
        start_ts = int(start.timestamp())
    else:
        start_ts = None

    if end:
        end_ts = int(end.timestamp())
    else:
        end_ts = None

    # filter by date
    if menuItem == 4:
        filtered_df = df

        if start_ts is not None:
            filtered_df = filtered_df[filtered_df["unixtime"] >= start_ts]

        if end_ts is not None:
            filtered_df = filtered_df[filtered_df["unixtime"] <= end_ts]

    else:
        filtered_df = df

    tree = AVLTree()

    for _, row in filtered_df.iterrows():
        post_data = {
            "subreddit": row["subreddit"],
            "title": row["title"],
            "id": row["username"],
            "unixtime": row["unixtime"],
            "score": row["score"]
        }
        tree.add(row["score"], post_data)

    return tree, filtered_df