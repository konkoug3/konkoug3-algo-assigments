import argparse
from itertools import permutations, combinations

# Βοηθητική: Από δυαδική συμβολοσειρά -> δείκτες μονάδων
def binary_string_to_indices(s):
    return [i for i, ch in enumerate(s) if ch == '1']

# Απόσταση Hamming μεταξύ λιστών δεικτών
def hamming_distance_indices(a, b):
    return sum(x != y for x, y in zip(a, b))

# Έλεγχος genlex μεταξύ διαδοχικών κόμβων
def is_genlex(path):
    for i in range(1, len(path)):
        if not all(p in path[i] for p in path[i - 1][:len(path[i - 1]) - 1]):
            return False
    return True

# Αναδρομικό DFS
def dfs(graph, current, visited, path, all_paths, all_nodes, indices_map):
    visited.add(current)
    path.append(current)

    if len(path) == len(all_nodes):
        all_paths.append(path[:])
    else:
        for neighbor in graph[current]:
            if neighbor not in visited:
                a = indices_map[current]
                b = indices_map[neighbor]
                if hamming_distance_indices(a, b) == 1:
                    if is_genlex([indices_map[n] for n in path] + [b]):
                        dfs(graph, neighbor, visited, path, all_paths, all_nodes, indices_map)

    visited.remove(current)
    path.pop()

# Δημιουργία κόμβων ως δυαδικές συμβολοσειρές και δεκαδικοί
def generate_nodes(s, t):
    perms = set(permutations('0'*s + '1'*t))
    bin_nodes = [''.join(p) for p in perms]
    unique_bin_nodes = sorted(set(bin_nodes))
    decimal_nodes = [int(b, 2) for b in unique_bin_nodes]
    return unique_bin_nodes, decimal_nodes

# Κατασκευή γράφου μεταθέσεων
def build_graph(s, t):
    bin_nodes, dec_nodes = generate_nodes(s, t)
    graph = {n: [] for n in dec_nodes}
    for i in range(len(bin_nodes)):
        for j in range(i+1, len(bin_nodes)):
            a, b = bin_nodes[i], bin_nodes[j]
            if sum(x != y for x, y in zip(a, b)) == 2:
                if sorted(a) == sorted(b):
                    a_dec = int(a, 2)
                    b_dec = int(b, 2)
                    graph[a_dec].append(b_dec)
                    graph[b_dec].append(a_dec)
    return graph, bin_nodes, dec_nodes

# DFS handler
def handle_dfs(s, t, start_node=None):
    graph, bin_nodes, dec_nodes = build_graph(s, t)
    indices_map = {int(b, 2): binary_string_to_indices(b) for b in bin_nodes}
    all_paths = []

    start_nodes = [start_node] if start_node is not None else dec_nodes
    for start in start_nodes:
        visited = set()
        path = []
        dfs(graph, start, visited, path, all_paths, dec_nodes, indices_map)

    for path in all_paths:
        binaries = [format(n, f'0{s+t}b') for n in path]
        indices_repr = [binary_string_to_indices(b) for b in binaries]
        print(binaries)
        print(indices_repr)
        print(path)

# Main πρόγραμμα
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('s', type=int)
    parser.add_argument('t', type=int)
    parser.add_argument('mode', choices=['graph', 'dfs', 'bts'])
    parser.add_argument('start', nargs='?', type=int)

    args = parser.parse_args()

    if args.mode == 'graph':
        graph, _, nodes = build_graph(args.s, args.t)
        for node in sorted(graph.keys(), reverse=True):
            neighbors = sorted(graph[node], reverse=True)
            print(f"{node} -> {neighbors}")
    elif args.mode == 'dfs':
        handle_dfs(args.s, args.t, args.start)
    elif args.mode == 'bts':
        print("BTS mode not implemented yet.")
