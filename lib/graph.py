from collections import defaultdict

"""
I got the majority of this code in the StackOverflow answer at
https://stackoverflow.com/a/30747003. I tweaked the code to handle
nodes without any connections and I added a method to find the
largest continuous subgraph (has a bug for specific conditions
in directed graphs, and could probably use a lot of optimization) 
"""

class Graph:
    def __init__(self, connections, directed = False):
        self._graph = defaultdict(set)
        self._directed = directed
        self.add_connections(connections)

    def add_connections(self, connections):
        for node1, node2 in connections:
            self.add(node1, node2)
    
    def add(self, node1, node2):
        if node2 != None:
            self._graph[node1].add(node2)
            if not self._directed:
                self._graph[node2].add(node1)
        elif len(self._graph[node1]) == 0:
            pass
            
    def remove(self, node):
        for n, cxns in self._graph.items():
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
        except KeyError:
            pass
    
    def is_connected(self, node1, node2):
        return node1 in self._graph and node2 in self._graph[node1]
    
    def find_path(self, node1, node2, path = []):
        # finds a path between nodes, not necessarily optimal
        path = path + [node1]
        if node1 == node2:
            return path
        if node1 not in self._graph:
            return None
        for node in self._graph[node1]:
            if node not in path:
                new_path =self.find_path(node, node2, path)
                if new_path:
                    return new_path
        return None

    def largest_subgraph(self):
        """
        there is a bug that a single edge coming into a directed 
        network isn't detected properly and probably heavily 
        optimizable
        """
        print("Identifying largest subgraph")
        networks = []
        all_nodes = list(self._graph)
        i = 1
        while all_nodes != []:
            print(f"Starting subgraph {i}")
            starting_node = all_nodes[0]
            visited_nodes = [starting_node]
            change = True
            while change:
                change = False
                for node in all_nodes:
                    for known in visited_nodes:
                        if node in self._graph[known] and node not in visited_nodes:
                            visited_nodes.append(node)
                            change = True
                all_nodes = [node for node in all_nodes if node not in visited_nodes]
            networks.append(set(visited_nodes))
            i += 1
            
        max_size = 0
        for network in networks:
            if len(network) == max_size:
                ambiguous = True
            if len(network) > max_size:
                ambiguous = False
                max_size = len(network)
                # currentLargest is just a list of the connected nodes,
                # the actual connections come from the original graph
                currentLargest = network
        largestNetwork = {}
        for key in self._graph:
            if key in currentLargest:
                largestNetwork.update({key: self._graph[key]})
        if ambiguous:
            print("There are multiple of the same size, one was chosen")
        return largestNetwork

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))

if __name__ == "__main__":
    from pprint import PrettyPrinter
    # connections = [('A', 'B'), ('B', 'C'), ('B', 'D'), ('C', 'D'), ('E', 'F')]
    # g = Graph(connections, directed = True)
    # # g.add('E', 'D')
    # # g.remove('A')
    # g.add('R', None)
    # g.add('A', 'Z')
    # pretty_print = PrettyPrinter()
    # pretty_print.pprint(g._graph)
    # pretty_print.pprint(g.largest_subgraph())

    # connections = [(1, 3), (3, 4), (4, 6), (4, 5), (5, 6), (6, 7), (1, 2), (2, 11), (11, 15),
    #                 (11, 12), (12, 13), (13, 16), (13, 14), (22, 23), (17, 18), (18, 19), (8, 9),
    #                 (8, 10), (30, 31), (34, 35), (35, 36), (37, None), (38, None), (39, None), (40, None),
    #                 (32, None), (33, None), (28, None), (29, None), (20, 21), (24, 25), (26, 27)]

    # g = Graph(connections, directed = True)

    # pprint = PrettyPrinter()
    # pprint.pprint(g.largest_subgraph())

    connections = [(1, None), (2, 3), (3, 4), (4, 2), (5, 2)]
    g = Graph(connections, directed = True)
    pprint = PrettyPrinter()
    pprint.pprint(g.largest_subgraph())