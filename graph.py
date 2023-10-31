from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

class BidirectionalSearch:
    def __init__(self, vertices):
        self.vertices = vertices
        self.graph = [set() for _ in range(vertices)]
        self.src_visited, self.dest_visited = set(), set()
        self.src_parent, self.dest_parent = [-1] * vertices, [-1] * vertices
        self.src_queue, self.dest_queue = deque(), deque()

    def add_edge(self, src, dest):
        self.graph[src].add(dest)
        self.graph[dest].add(src)

    def bfs(self, queue, visited, parent, direction):
        current = queue.popleft()
        for vertex in self.graph[current]:
            if vertex not in visited:
                queue.append(vertex)
                visited.add(vertex)
                parent[vertex] = current

    def is_intersecting(self):
        return self.src_visited.intersection(self.dest_visited).pop() if self.src_visited.intersection(self.dest_visited) else -1


    def print_path(self, intersecting_node, src, dest):
        path = []

        # Traverse the path from source to intersection
        i = intersecting_node
        while i != -1:
            path.append(i)
            i = self.src_parent[i]

        # Traverse the path from destination to intersection
        path.append('\n')
        i = intersecting_node
        while i != -1:
            path.append(i)
            i = self.dest_parent[i]

        print("**Path**")
        print(' '.join(map(str, reversed(path))))


    def bidirectional_search(self, src, dest):
        self.src_queue.append(src)
        self.src_visited.add(src)
        self.src_parent[src] = -1

        self.dest_queue.append(dest)
        self.dest_visited.add(dest)
        self.dest_parent[dest] = -1

        while self.src_queue and self.dest_queue:
            self.bfs(self.src_queue, self.src_visited, self.src_parent, 'forward')
            self.bfs(self.dest_queue, self.dest_visited, self.dest_parent, 'backward')
            intersecting_node = self.is_intersecting()
            if intersecting_node != -1:
                print(f"Path exists between {src} and {dest}")
                print(f"Intersection at: {intersecting_node}")
                self.print_path(intersecting_node, src, dest)
                return

        print(f"Path does not exist between {src} and {dest}")
    def visualize_graph(self):
        G = nx.Graph()
        for src in range(self.vertices):
            for dest in self.graph[src]:
                G.add_edge(src, dest)

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8, font_color='black')
        plt.show()
        
# Driver code
if __name__ == '__main__':
    n = 15
    src, dest = 1,14
    graph = BidirectionalSearch(n)
    edges = [(0, 4), (1, 4), (2, 5), (3, 5), (4, 6), (5, 6), (6, 7), (7, 8), (8, 9), (8, 10), (9, 11), (9, 12), (10, 13), (10, 14)]

    for edge in edges:
        graph.add_edge(*edge)
    graph.visualize_graph()
    graph.bidirectional_search(src, dest)