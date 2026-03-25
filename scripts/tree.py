from graphviz import Digraph
from datetime import datetime

class AVLNode:
    def __init__(self, score, post):
        self.score = score
        self.posts = [post]   # store multiple posts with same score
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    
    def insert(self, node, score, post):
        if not node:
            return AVLNode(score, post)
        if score < node.score:
            node.left = self.insert(node.left, score, post)
        elif score > node.score:
            node.right = self.insert(node.right, score, post)
        else:
            node.posts.append(post)
            return node

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        # Balance tree
        if balance > 1 and score < node.left.score:
            return self.right_rotate(node)
        if balance < -1 and score > node.right.score:
            return self.left_rotate(node)
        if balance > 1 and score > node.left.score:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        if balance < -1 and score < node.right.score:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def add(self, score, post):
        self.root = self.insert(self.root, score, post)

    
    # Search and Filtering
    def search(self, node, score):
        if not node:
            return None
        if score == node.score:
            return node.posts
        elif score < node.score:
            return self.search(node.left, score)
        else:
            return self.search(node.right, score)

    @staticmethod
    def filter_bytime(posts, start_date=None, end_date=None):
        #Filter posts by datetime (optional) 
        if start_date:
            start_ts = int(start_date.timestamp())
        else:
            start_ts = None
        if end_date:
            end_ts = int(end_date.timestamp())
        else:
            end_ts = None

        filtered = []
        for post in posts:
            t = post.get("unixtime")
            if t is None:
                continue
            if start_ts is not None and t < start_ts:
                continue
            if end_ts is not None and t > end_ts:
                continue
            filtered.append(post)
        return filtered

    def find_by_score(self, score, start_date=None, end_date=None):
        node_posts = self.search(self.root, score)
        if not node_posts:
            return []
        return self.filter_bytime(node_posts, start_date, end_date)

    def range_query(self, node, low, high, result, start_date=None, end_date=None):
        if not node:
            return
        if low < node.score:
            self.range_query(node.left, low, high, result, start_date, end_date)
        if low <= node.score <= high:
            result.extend(self.filter_bytime(node.posts, start_date, end_date))
        if node.score < high:
            self.range_query(node.right, low, high, result, start_date, end_date)

    def check_range(self, low, high, start_date=None, end_date=None):
        result = []
        self.range_query(self.root, low, high, result, start_date, end_date)
        return result


    # Return Top-k posts
    def reverse_inorder(self, node, result, k, start_date=None, end_date=None):
        if not node or len(result) >= k:
            return
        self.reverse_inorder(node.right, result, k, start_date, end_date)
        for post in self.filter_bytime(node.posts, start_date, end_date):
            if len(result) < k:
                result.append((node.score, post))
            else:
                break
        self.reverse_inorder(node.left, result, k, start_date, end_date)

    def top_k(self, k, start_date=None, end_date=None):
        result = []
        self.reverse_inorder(self.root, result, k, start_date, end_date)
        return result[:k]

    # Sorted posts
    def inorder(self, node, result):
        if not node:
            return
        self.inorder(node.left, result)
        result.append((node.score, node.posts))
        self.inorder(node.right, result)

    def get_sorted_posts(self):
        result = []
        self.inorder(self.root, result)
        return result


    # Create visualization
    def export_graphviz(self, node, dot=None, depth=0, max_depth=4):
        if dot is None:
            dot = Digraph()
            dot.attr('node', shape='box', style='filled', fontname='Arial')

        if node is None or depth > max_depth:
            return dot

        balance = self.get_balance(node)
        color = "tomato" if balance < 0 else ("lightblue" if balance == 1 else "lightgreen")

        sample_title = node.posts[0]["title"] if node.posts else ""
        sample_title = (sample_title[:30] + "...") if len(sample_title) > 30 else sample_title

        label = f"""Score: {node.score}
Depth: {depth}
Posts: {len(node.posts)}
H: {node.height}
BF: {balance}
Title: {sample_title}"""

        node_id = f"{node.score}_{depth}"
        dot.node(node_id, label, fillcolor=color)

        if node.left:
            left_id = f"{node.left.score}_{depth+1}"
            dot.edge(node_id, left_id)
            self.export_graphviz(node.left, dot, depth+1, max_depth)
        if node.right:
            right_id = f"{node.right.score}_{depth+1}"
            dot.edge(node_id, right_id)
            self.export_graphviz(node.right, dot, depth+1, max_depth)

        return dot