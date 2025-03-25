graph = {
    1: {"duration": 9, "predecessors": set(), "successors": {4, 5}},
    2: {"duration": 2, "predecessors": set(), "successors": {3, 10}},
    3: {"duration": 3, "predecessors": {2}, "successors": {10}},
    4: {"duration": 5, "predecessors": {1}, "successors": {5, 7, 8, 9}},
    5: {"duration": 2, "predecessors": {1, 4}, "successors": {6, 8, 11}},
    6: {"duration": 2, "predecessors": {5}, "successors": {11}},
    7: {"duration": 2, "predecessors": {4}, "successors": {11}},
    8: {"duration": 4, "predecessors": {4, 5}, "successors": {11}},
    9: {"duration": 5, "predecessors": {4}, "successors": {}},
    10: {"duration": 1, "predecessors": {2, 3}, "successors": {}},
    11: {"duration": 2, "predecessors": {1, 5, 6, 7, 8}, "successors": {}},
}

def parse_constraint_file(filename):
    graph = {}
    with open(filename, "r") as file:
        for line in file:
            parts = list(map(int, line.split()))  # Convert to integers

            node = parts[0]  # Task number
            duration = parts[1]  # cost (duration)
            predecessors = set(parts[2:]) if len(parts) > 2 else set()
            graph[node] = {"duration": duration, "predecessors": predecessors, "successors": set()}

    # Compute successors by scanning predecessors
    for node, data in graph.items():
        for pred in data["predecessors"]:
            graph[pred]["successors"].add(node)

    return graph

def display_graph(graph):
    print("Creating the scheduling graph:\n")
    print(f"{len(graph.keys())} vertices")
    print(sum(len(data["successors"]) for data in graph.values()), "edges\n")
    for nodes, edges in graph.items():
        print(f"{nodes} -> {edges["successors"]} = {edges["duration"]}")
    return print("\n-- End of graph --")


display_graph(parse_constraint_file("table 1.txt"))



