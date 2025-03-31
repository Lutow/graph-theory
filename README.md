# 📊 Scheduling Optimization with Graph Theory

## 📝 Project Overview
This project implements scheduling optimization using **Graph Theory**, focusing on parsing constraint files, detecting conflicts, and calculating critical paths. The primary objective is to create an efficient scheduling graph that handles task durations, dependencies, and ranks effectively.

## 🔍 Key Features
- **Graph Parsing**: Reads constraint files and builds a scheduling graph with nodes, durations, predecessors, and successors.
- **Cycle & Conflict Detection**:
  - Detects negative durations in tasks.
  - Identifies cycles in the graph, ensuring feasibility for further computations.
- **Schedule Computations**:
  - Computes ranks, earliest and latest dates, and task floats.
  - Determines the critical path using float analysis.

## 🚀 Core Algorithms & Methods
### Code Highlights:
- **`parse_constraint_file`**: Parses constraint files to store graph data efficiently in memory as dictionaries.
- **`detect_cycle` & `detect_negative_edges`**: Validates the graph by checking for cycles and negative task durations.
- **`compute_ranks`**: Determines task ranks using level-order traversal of the graph.
- **Critical Path Analysis**: Utilizes float computations to identify the tasks on the critical path.

### Scheduling Outputs:
- Task ranks, earliest and latest dates, value matrix, and critical path visualization for optimized scheduling.

---

## 🛠️ Tools & Technologies
- **Language**: Python
- **Libraries**: `collections`, basic Python sets and dictionaries
- **Code Components**:
  - Parsing graph structures from `.txt` files.
  - Visualization tools to display the graph and value matrix.

## 📈 Impact
The project demonstrates the power of graph-based algorithms in solving scheduling problems, ensuring tasks are completed efficiently and dependencies are respected. It highlights the versatility of graph theory for real-world applications like project management and workflow optimization.

---

Feel free to enhance this README by adding specific examples or outputs from your project! 😊
