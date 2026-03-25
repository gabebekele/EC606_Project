import time
import math
from datetime import datetime
from load_data import build_tree


def test_prog():
    print("Building AVL tree...")
    start = time.perf_counter()

    tree, df = build_tree("submissions.csv")

    end = time.perf_counter()
    print("Build complete.")
    print("Total posts:", len(df))
    print("Build time:", end - start)
    print("Tree height:", tree.get_height(tree.root))

    # Time period filter (optional)
    start_period = datetime(2012, 3, 1)
    end_period = datetime(2015, 3, 31, 23, 59, 59)

    # Exact score query
    function_testscore = df.iloc[100]["score"]
    posts = tree.find_by_score(function_testscore, start_date=start_period, end_date=end_period)
    print_query_results("Find posts with", posts, score=function_testscore, start_date=start_period, end_date=end_period)

    # Score range query
    low_score, high_score = 300, 400
    posts_range = tree.check_range(low_score, high_score, start_date=start_period, end_date=end_period)
    print_query_results("Search posts in score", posts_range, low=low_score, high=high_score, start_date=start_period, end_date=end_period)

    # Top-k posts
    top_posts = tree.top_k(10, start_date=start_period, end_date=end_period)
    top_posts_only = [post for _, post in top_posts]  # extract just posts
    print_query_results("Top posts", top_posts_only, top_k=10, start_date=start_period, end_date=end_period)

    # Sorted order check
    sorted_nodes = tree.get_sorted_posts()
    scores = [score for score, _ in sorted_nodes]
    print("\nTesting sorted order...")
    print("Is sorted correctly:", scores == sorted(scores))

    # Summary stats
    print("\nSummary:")
    print("Lowest score:", sorted_nodes[0][0])
    print("Highest score:", sorted_nodes[-1][0])
    print("Unique score values:", len(sorted_nodes))

    # Create PNG visualization
    print("\nCreate PNG visualization (limited depth)...")
    dot = tree.export_graphviz(tree.root, max_depth=3)
    dot.render("avl_tree", format="png", cleanup=True)


if __name__ == "__main__":
    test_prog()