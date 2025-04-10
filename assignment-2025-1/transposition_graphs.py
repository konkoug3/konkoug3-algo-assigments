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

def is_homogeneous(a, b, length):
    return sum(1 for x, y in zip(to_binary(a, length), to_binary(b, length)) if x != y) == 1

def dfs(graph, current, visited, path, all_paths, total_nodes, length):
    visited.add(current)
    path.append(current)
    if len(path) == total_nodes:
        all_paths.append(list(path))
    else:
        for neighbor in graph[current]:
            if neighbor not in visited:
                if is_homogeneous(current, neighbor, length) and is_genlex(path, neighbor, length):
                    dfs(graph, neighbor, visited, path, all_paths, total_nodes, length)
    visited.remove(current)
    path.pop()

def sigma_j(j, s, t):
    bin_j = format(j, f'0{s - 1}b')
    tail = ''.join('-' if bit == '1' else '+' for bit in bin_j)
    return '0' * t + tail

def next_bts(s):
    results = []
    for j in range(2 ** (s - 1)):
        state = list(sigma_j(j, s, t))
        sequence = []
        seen = set()
        while tuple(state) not in seen:
            seen.add(tuple(state))
            sequence.append(''.join(state))
            state = next_ternary(state)
        results.append(sequence)
    return results

def next_ternary(s):
    s = s.copy()
    i = len(s) - 1
    while i >= 2:
        if s[i - 2] == '0' and s[i - 1] == '-' and s[i] == '+':
            s[i - 2], s[i - 1], s[i] = '-', '+', '0'
            if i + 1 < len(s) and s[i + 1] in '+-':
                s[i + 1] = '0'
            break
        elif s[i - 2] == '+' and s[i - 1] == '-' and s[i] == '0':
            s[i - 2], s[i - 1], s[i] = '0', '+', '-'
            if i + 1 < len(s) and s[i + 1] in '+-':
                s[i + 1] = '0'
            break
        i -= 1
    return s

def bts_to_binary(s):
    return ''.join('1' if c == '0' else '0' for c in s)

def bts_mode(s, t):
    all_sequences = next_bts(s)
    length = s + t
    for sequence in all_sequences:
        binaries = [bts_to_binary(x) for x in sequence]
        ints = [int(x, 2) for x in binaries]
        index_repr = [indices(n, length) for n in ints]
        print(sequence)
        print(binaries)
        print(index_repr)
        print(ints)

def print_graph(graph):
    for node in sorted(graph.keys(), reverse=True):
        neighbors = sorted(graph[node], reverse=True)
        print(f"{node} -> {neighbors}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("s", type=int)
    parser.add_argument("t", type=int)
    parser.add_argument("mode", choices=["graph", "dfs", "bts"])
    parser.add_argument("start", nargs="?", type=int)
    args = parser.parse_args()
    global t
    t = args.t
    length = args.s + args.t

    if args.mode == "graph":
        graph = build_graph(args.s, args.t)
        print_graph(graph)
    elif args.mode == "dfs":
        graph = build_graph(args.s, args.t)
        start_node = args.start if args.start is not None else max(graph.keys())
        all_paths = []
        dfs(graph, start_node, set(), [], all_paths, len(graph), length)
        for path in all_paths:
            binaries = [to_binary(n, length) for n in path]
            indexes = [indices(n, length) for n in path]
            print(binaries)
            print(indexes)
            print(path)
    elif args.mode == "bts":
        bts_mode(args.s, args.t)

if __name__ == "__main__":
    main()
