def parse_constraint_file(filename):
    graph = {}
    graph[0] = {"duration": 0, "predecessors": set(), "successors": set()}
    with open(filename, "r") as file:
        for line in file:
            parts = list(map(int, line.split()))

            node = parts[0]
            duration = parts[1] 
            predecessors = set(parts[2:]) if len(parts) > 2 else set()

            graph[node] = {
                "duration": duration,
                "predecessors": predecessors,
                "successors": set()
            }

    start_tasks = {node for node, data in graph.items() if node != 0 and not data["predecessors"]}
    graph[0]["successors"] = start_tasks 

    for task in start_tasks:
        graph[task]["predecessors"].add(0)

    for node, data in graph.items():
        for pred in data["predecessors"]:
            graph[pred]["successors"].add(node)

    end_tasks = {node for node, data in graph.items() if not data["successors"]}

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
    print(" -> ".join(map(str, cp)))
    return cp
    

while True:
    TableNumber = int(input("Please enter an integer between 1 and 15 to choose your table: "))
    while TableNumber > 15 or TableNumber < 1:
        TableNumber = int(input("Please enter an integer between 1 and 15 to choose your table: "))
    graph = parse_constraint_file("Table testing/table "+ str(TableNumber)+ ".txt")
    print("\n")
    display_graph(graph)
    if not detect_cycle(graph) or not detect_negative_edges(graph):
        print("We made sure that we have no negative durations or cycles which means we can now do the other computations.\n")
        print("Ranks :\n" + str(compute_ranks(graph)) + "\n")
        display_value_matrix(graph)
        print("Earliest dates table : \n   " + str(earliest_dates(graph)) + "\n")
        print("Latest dates table : \n   " +str(latest_dates(graph)) + "\n")
        print("Floats table : \n   " + str(compute_float(graph)) + "\n")
        print("Critical path : \n  ", end= " ")
        critical_path(compute_float(graph), graph)
    elif detect_cycle(graph):
        print("This graph contains at least a cycle, this means we cannot do any further computations.\n")
    elif detect_negative_edges(graph):
        print("This graph contains negative durations, this means we cannot do any further computation.\n")
    x = input("Do you want to work on another table ? Y/N \n")
    if x == "N":
        break