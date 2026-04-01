REDDIT RANKER

Reddit Post Indexing with AVL Tree

OVERVIEW

This project implements an AVL Tree (self-balancing binary search tree) to efficiently index and query thousands of Reddit posts based on their score.

The system supports fast insertion, searching, score-based queries, optional time-based filtering using Unix timestamps, and visualization of the tree structure.

FEATURES

Query Capabilities:

-Find posts by exact score
-Find posts within a score range [X, Y]
-Retrieve top-k highest scoring posts
-Optional filtering by date range

AVL Tree Properties:

Automatically balances after each insertion
Maintains height O(log n)
Stores multiple posts with the same score in a single node

Time Filtering:

Uses Unix timestamps for efficient comparison
Supports filtering by start date, end date, or both

DATASET

The dataset contains Reddit submissions and includes:

-score
-title
-subreddit
-username
-rawtime
-Unixtime

INSTALLATION

Clone the repository:
git clone https://github.com/yourusername/reddit-avl-tree.git

cd reddit-avl-tree
Install required libraries:
pip install pandas graphviz
Install Graphviz (required for visualization):
Download from https://graphviz.org/download/

Make sure the "dot" executable is added to your system PATH.

HOW TO RUN

Run the program using:
python app.py

USER INTERFACE

The program provides a command-line interface with the following options:

1: Find posts by exact score
2: Find posts in a score range
3: Top-k posts by score
4: Show AVL tree visualization (PNG)
0: Exit

Example inputs:

Score: 100
Range: 300 to 400
Top-k: 10
Date format: YYYY-MM-DD

HOW IT WORKS

AVL Tree Structure:
Each node stores score (key), a list of posts with that score, the left, and right children, and the height

Time Handling:

rawtime is converted to datetime, datetime is converted to Unixtime, all filtering is done using Unix timestamps

TIME COMPLEXITY

Insert: O(log n)
Search: O(log n)
Range Query: O(log n + k)
Top-k Query: O(log n + k)

VISUALIZATION

The AVL tree can be exported as a PNG file showing the score, depth, number of posts, height, balance factor, and a sample post title

The output file is saved as avl_tree.png

INPUT VALIDATION

Users must use the format YYYY-MM-DD for the dates. Invalid inputs are handled without crashing the program and users are prompted to re-enter values

EXAMPLE OUTPUT

Find posts with score = 13 in a given time period
Number of posts: 1385

Score: 13, Title: Example post title

FUTURE IMPROVEMENTS

The first major improvement would to implement a graphical user interface to add to the aesthetics of the program. I would also like to add the ability to store data in a database. Performance comparisons with other data structures would also be a good addition to the product.


REFERENCES

- https://www.geeksforgeeks.org/python/how-to-convert-datetime-to-unix-timestamp-in-python/

- https://graphviz.readthedocs.io/en/stable/manual.html

- https://www.w3schools.com/python/python_user_input.asp