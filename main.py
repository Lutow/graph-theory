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

    # Step 1: Add fictitious start node (0) first
    graph[0] = {"duration": 0, "predecessors": set(), "successors": set()}

    # Step 2: Read file and construct basic graph
    with open(filename, "r") as file:
        for line in file:
            parts = list(map(int, line.split()))  # Convert to integers

            node = parts[0]  # Task number
            duration = parts[1]  # Duration (cost)
            predecessors = set(parts[2:]) if len(parts) > 2 else set()

            graph[node] = {
                "duration": duration,
                "predecessors": predecessors,
                "successors": set()
            }

    # Step 3: Identify tasks with no predecessors → They should depend on node 0
    start_tasks = {node for node, data in graph.items() if node != 0 and not data["predecessors"]}
    graph[0]["successors"] = start_tasks  # Link α to these tasks

    for task in start_tasks:
        graph[task]["predecessors"].add(0)

    # Step 4: Establish successor relationships
    for node, data in graph.items():
        for pred in data["predecessors"]:
            graph[pred]["successors"].add(node)

    # Step 5: Identify nodes with no successors → They should lead to node N+1 (ω)
    end_tasks = {node for node, data in graph.items() if not data["successors"]}

    # Step 6: Define fictitious end node (ω) at the **end**
    omega = max(graph.keys()) + 1  # N+1
    graph[omega] = {"duration": 0, "predecessors": end_tasks, "successors": set()}

    for task in end_tasks:
        graph[task]["successors"].add(omega)

    return graph


def detect_negative_edges(graph):
    for node, data in graph.items():
        if data["duration"] < 0:
            return True, print("Negative duration detected\n")
        else:
            return False, print("No negative duration detected\n")


def display_graph(graph):
    print("Creating the scheduling graph:\n")
    print(f"{len(graph.keys())} vertices")
    print(sum(len(data["successors"]) for data in graph.values()), "edges\n")
    detect_negative_edges(graph)
    last = max(graph.keys())
    for nodes, edges in graph.items():
        if nodes != last:
            print(f"{nodes} -> {edges['successors']} = {edges['duration']}")
    return print("\n-- End of graph --")


display_graph(parse_constraint_file("table 1.txt"))

def detect_cycle(graph):
    def dfs(node, visited, rec_stack):
        visited.add(node)
        rec_stack.add(node)
        for successor in graph[node]["successors"]:
            if successor not in visited:
                if dfs(successor, visited, rec_stack):
                    return True
            elif successor in rec_stack:
                return True
        rec_stack.remove(node)
        return False

    visited = set()
    rec_stack = set()
    for node in graph:
        if node not in visited and node != 0 and node != max(graph.keys()):
            if dfs(node, visited, rec_stack):
                return True
    return False

def display_value_matrix(graph):
    nodes = sorted(graph.keys())  # Get sorted task numbers
    matrix = [["*" for _ in nodes] for _ in nodes]  # Initialize matrix

    for node in nodes:
        for predecessor in graph[node]["predecessors"]:
            node_idx = nodes.index(node)
            predecessor_idx = nodes.index(predecessor)
            matrix[predecessor_idx][node_idx] = graph[predecessor]["duration"]
    print("\nValue Matrix:\n")
    header = "   " + "  ".join(f"{node:>2}" for node in nodes)
    print(header)
    for i, row in enumerate(matrix):
        row_str = f"{nodes[i]:>2} " + "  ".join(f"{val:>2}" for val in row)
        print(row_str)

def compute_ranks(graph):
    if not detect_cycle(graph):
        from collections import deque

        # Initialize in-degree of each vertex
        in_degree = {node: len(graph[node]["predecessors"]) for node in graph}
        queue = deque([node for node in graph if in_degree[node] == 0])
        rank = {}
        current_rank = -1 #We set up a initial value of -1 so our ranking computation loop starts at value 0 

        while queue:
            current_rank += 1
            for _ in range(len(queue)):
                node = queue.popleft()
                rank[node] = current_rank
                for successor in graph[node]["successors"]:
                    in_degree[successor] -= 1
                    if in_degree[successor] == 0:
                        queue.append(successor)

        return rank
    else:

        print("A cycle has been detect, unable to compute rank !")


def earliest_dates(graph):
    ESD = {node: 0 for node in graph}  
    for node in sorted(graph.keys()):  
        if graph[node]["predecessors"]:  
            ESD[node] = max(ESD[p] + graph[p]["duration"] for p in graph[node]["predecessors"])
    return ESD 


def latest_dates(graph):
    LD = {node: earliest_dates(graph)[node] for node in graph}
    for node in sorted(graph.keys(), reverse=True):
        if graph[node]["successors"]:
            LD[node] = min(LD[s] for s in graph[node]["successors"]) - graph[node]["duration"]
    return LD
    

def compute_float(graph):
    return {node: latest_dates(graph)[node] - earliest_dates(graph)[node] for node in graph}



def critical_path(floats, graph):
    cp = [node for node in floats if floats[node] == 0 and graph[node]["duration"] > 0]
    return cp
    

while True:
    TableNumber = int(input("Please enter an integer between 1 and 15 to choose your table: "))
    while TableNumber > 15 or TableNumber < 1:
        TableNumber = int(input("Please enter an integer between 1 and 15 to choose your table: "))
    x = 1
    while x < 7:
        x = int(input("What do you want to do with this graph ? \n"
              "1. Display the graph\n"
              "2. Display the value matrix and get the ranks\n"
              "3. Execute the negative condition and cycle checks\n"
              "4. Compute the earliest date calendar\n"
              "5. Compute the latest date calendar\n"
              "6. Compute the floats\n"
              "7. Try another with another table"))
        if x == 1:
            display_graph(parse_constraint_file("Table testing/table "+ str(TableNumber)+ ".txt"))
        elif x == 2:
            ranks = compute_ranks(parse_constraint_file("Table testing/table " + str(TableNumber) + ".txt"))
            display_value_matrix(parse_constraint_file("Table testing/table " + str(TableNumber) + ".txt"))
            if ranks:
                for node, r in ranks.items():
                    if node != 1 and node != 12:
                        print(f"Vertex {node}: Rank {r}")
            else:
                print("There is a cycle so we cannot compute the ranks.")
        elif x == 3:
            print("Negative condition check is: " + str(
                detect_negative_edges(parse_constraint_file("Table testing/table " + str(TableNumber) + ".txt"))))
            print("Cycle condition check is: " + str(
                detect_cycle(parse_constraint_file("Table testing/table " + str(TableNumber) + ".txt"))))
        elif x == 4:
            earliest_dates = compute_earliest_dates(graph)
            for node, date in earliest_dates.items():
                print(f"Task {node}: Earliest Start Time = {date}")
            """
                earliest
            elif x == 5:
                latest
            elif x == 6:
                floats
                    """
