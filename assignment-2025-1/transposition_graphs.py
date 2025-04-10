import argparse
from itertools import combinations
from collections import defaultdict

def generate_nodes(s, t):
    n = s + t
    result = []
    for ones in combinations(range(n), t):
        num = 0
        for i in range(n):
            if i in ones:
                num |= 1 << (n - 1 - i)
        result.append(num)
    return result

def hamming_distance(a, b):
    return bin(a ^ b).count("1")

def build_graph(s, t):
    nodes = generate_nodes(s, t)
    graph = defaultdict(list)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if hamming_distance(nodes[i], nodes[j]) == 2:
                graph[nodes[i]].append(nodes[j])
                graph[nodes[j]].append(nodes[i])
    return graph

def to_binary(n, length):
    return format(n, f'0{length}b')

def indices(n, length):
    return [i for i, bit in enumerate(to_binary(n, length)) if bit == '1']

def is_genlex(path, next_node, length):
    next_indices = indices(next_node, length)
    for i in range(1, len(path) + 1):
        current_indices = indices(path[-i], length)
        if current_indices[:i] != next_indices[:i]:
            return False
    return True

def dfs(graph, current, visited, path, all_paths, total_nodes, length):
    visited.add(current)
    path.append(current)
    print(f"DFS στον κόμβο {current}, διαδρομή: {path}")

    if len(path) == total_nodes:
        print("✅ Βρέθηκε πλήρης διαδρομή!")
        all_paths.append(list(path))
    else:
        for neighbor in graph[current]:
            if neighbor not in visited and hamming_distance(current, neighbor) == 2:
                if is_genlex(path, neighbor, length):
                    print(f"➡️ Πάμε από {current} στο {neighbor}")
                    dfs(graph, neighbor, visited, path, all_paths, total_nodes, length)
                else:
                    print(f"❌ genlex από {current} σε {neighbor} απορρίφθηκε")
            else:
                 print(f"❌ δεν πάμε από {current} σε {neighbor} (είτε επισκέφθηκε, είτε όχι Hamming=2)")
    visited.remove(current)
    path.pop()

def print_graph(graph):
    for node in sorted(graph.keys(), reverse=True):
        neighbors = sorted(graph[node], reverse=True)
        print(f"{node} -> {neighbors}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("s", type=int, help="Πλήθος μηδενικών")
    parser.add_argument("t", type=int, help="Πλήθος άσων")
    parser.add_argument("mode", choices=["graph", "dfs", "bts"], help="Τρόπος λειτουργίας")
    parser.add_argument("start", nargs="?", type=int, help="Αρχικός κόμβος για DFS")

    args = parser.parse_args()
    length = args.s + args.t

    if args.mode == "graph":
        graph = build_graph(args.s, args.t)
        print_graph(graph)

    elif args.mode == "dfs":
        graph = build_graph(args.s, args.t)
        start_node = args.start if args.start is not None else max(graph.keys())
        all_paths = []
        dfs(graph, start_node, set(), [], all_paths, len(graph), length)

        if not all_paths:
            print("Δεν βρέθηκε διαδρομή.")
        else:
            for path in all_paths:
                binary_path = [to_binary(n, length) for n in path]
                index_path = [[i for i, bit in enumerate(b) if bit == '1'] for b in binary_path]
                print(binary_path)
                print(index_path)
                print(path)

    elif args.mode == "bts":
        print("BTS mode not implemented yet.")

if __name__ == "__main__":
    main()
