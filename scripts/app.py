import math
from graphviz import Digraph
from datetime import datetime
from load_data import build_tree

def print_query_results(title, posts, score=None, low=None, high=None, start_date=None, end_date=None, top_k=None):
    
    # Print query results
    if start_date and end_date:
        period_text = (f" posted between {start_date} - {end_date}")
    elif start_date:
        period_text = (f" posted after {start_date}")
    elif end_date:
        period_text = (f" posted before {end_date}")
    else:
        period_text = ""
    
    # Build header
    header = title
    if score is not None:
        header += f" score={score}"
    if low is not None and high is not None:
        header += f" range=[{low}, {high}]"
    if top_k is not None:
        header += f" top-{top_k}"
    header += period_text
    
    print("\nNumber of posts:", len(posts))
    
    # Print all scores and titles for these
    if len(posts) <= 50:
       print(f"\n{header}")
       for p in posts:
            score_val = p.get("score", "N/A")
            title_val = p.get("title", "N/A")
            print(f"Score: {int(score_val)}, Title: {title_val}") 
    
    # Print first 50 posts if too many
    else:
        header += " — displaying the first 50 titles\n"
        print(f"{header}")
        for p in posts[:50]:
            score_val = p.get("score", "N/A")
            title_val = p.get("title", "N/A")
            print(f"Score: {int(score_val)}, Title: {title_val}")
           


def user_interface():
    print("\nLoading Reddit posts AVL Tree...")
    tree, df = build_tree("submissions.csv")
    avlheight = tree.get_height(tree.root)
    numPosts = len(df)
    print(f"Tree built with {numPosts} posts. Height: {avlheight}")

    while True:
        print("\n--- Reddit Post Query Menu ---")
        print("1: Find posts by exact score")
        print("2: Find posts in a score range")
        print("3: Top-k posts by score")
        print("4: Show AVL tree visualization (PNG)")
        print("0: Exit")
        
        choice = input("Enter option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break

        # Optional date filter
        start_str = input("Start date (YYYY-MM-DD) [optional]: ").strip()
        end_str = input("End date (YYYY-MM-DD) [optional]: ").strip()
        start_date = datetime.fromisoformat(start_str) if start_str else None
        end_date = datetime.fromisoformat(end_str) if end_str else None

        
        if choice == "1":
            while True:
                inputScore = input("Enter desired score: ")
                if not inputScore.isdigit():
                    print(f"Invalid input. Please enter a positive integer.\n")
                    continue

                score = int(inputScore)
                posts = tree.find_by_score(score, start_date, end_date)

                break

            print_query_results(
                "Find posts with",
                posts,
                score=score,
                start_date=start_date,
                end_date=end_date
            )

        elif choice == "2":
            while True:
                inputLow = input("Enter low score: ")
                if not inputLow.isdigit():
                    print(f"Invalid input. Please enter a number between 1 and {numPosts}.\n")
                    continue
                inputHigh = input("Enter high score: ")
                if not inputHigh.isdigit():
                    print(f"Invalid input. Please enter a number between 1 and {numPosts}.\n")
                    continue

                

                low = int(inputLow)
                high = int(inputHigh)
                posts = tree.check_range(low, high, start_date, end_date)
                
                break

            print_query_results(
                    "Search in score",
                    posts,
                    low=low,
                    high=high,
                    start_date=start_date,
                    end_date=end_date
                )

        elif choice == "3":

            while True:
                inputK = input("Enter k: ")
                if not inputK.isdigit():
                    print(f"Invalid input. Please enter a number between 1 and {numPosts}.\n")
                    continue

                k = int(inputK)
                if k <= 0 or k > numPosts:
                    print(f"Invalid input. Please enter a number between 1 and {numPosts}.\n")
                    continue

                break

            top_posts = tree.top_k(k, start_date, end_date)
            top_posts_only = [post for _, post in top_posts]
            print_query_results(
                "Top posts",
                top_posts_only,
                top_k=k,
                start_date=start_date,
                end_date=end_date
            )

        elif choice == "4":

            while True:
                depth_input = input(f"What would you like the AVL tree depth to be? (1–{avlheight}, default=3): ").strip()

                # Default value
                if depth_input == "":
                    depth = 3
                else:
                    # Ensure it is a number
                    if not depth_input.isdigit():
                        print(f"Invalid input. Please enter a number between 1 and {avlheight}.\n")
                        continue

                    depth = int(depth_input)

                    # Validate range
                    if depth <= 0 or depth > avlheight:
                        print(f"Invalid input. Please enter a number between 1 and {avlheight}.\n")
                        continue
                
                break

            print(f"Generating AVL tree PNG (depth = {depth})...")
            dot = tree.export_graphviz(tree.root, max_depth=depth)
            dot.render("avl_tree", format="png", cleanup=True)
            print("Tree saved as 'avl_tree.png'")

        

if __name__ == "__main__":
    user_interface()