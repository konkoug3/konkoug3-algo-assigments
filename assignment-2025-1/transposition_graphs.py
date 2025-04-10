import argparse
from itertools import combinations
from collections import defaultdict
from collections import deque

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
    a_idx = indices(a, length)
    b_idx = indices(b, length)
    return len(set(a_idx) ^ set(b_idx)) == 2

def dfs(graph, current, visited, path, all_paths, total_nodes, length):
    visited.add(current)
    path.append(current)
    if len(path) == total_nodes:
        all_paths.append(list(path))
    else:
        for neighbor in sorted(graph[current], reverse=True):
            if neighbor not in visited and is_homogeneous(current, neighbor, length) and is_genlex(path, neighbor, length):
                dfs(graph, neighbor, visited, path, all_paths, total_nodes, length)
    visited.remove(current)
    path.pop()

def print_graph(graph):
    for node in sorted(graph.keys(), reverse=True):
        neighbors = sorted(graph[node], reverse=True)
        print(f"{node} -> {neighbors}")

def sigma_j(j, s, t):
    bin_j = format(j, f'0{s - 1}b')
    tail = ''.join('-' if bit == '1' else '+' for bit in bin_j)
    return '0' * t + tail

def next_ternary(s):
    s = list(s)
    for i in reversed(range(2, len(s))):
        if s[i - 2:i + 1] == ['0', '-', '+']:
            s[i - 2:i + 1] = ['-', '+', '0']
            for j in range(i + 1, len(s)):
                if s[j] in '+-':
                    s[j] = '0'
                    break
            return ''.join(s)
        elif s[i - 2:i + 1] == ['+', '-', '0']:
            s[i - 2:i + 1] = ['0', '+', '-']
            for j in range(i + 1, len(s)):
                if s[j] in '+-':
                    s[j] = '0'
                    break
            return ''.join(s)
    return None

def bts_to_binary(s):
    return ''.join('1' if c == '0' else '0' for c in s)

def bts_mode(s, t):
    length = s + t
    for j in range(2 ** (s - 1)):
        seq = []
        state = sigma_j(j, s, t)
        seen = set()
        while state and state not in seen:
            seen.add(state)
            seq.append(state)
            state = next_ternary(state)
        binaries = [bts_to_binary(x) for x in seq]
        ints = [int(x, 2) for x in binaries]
        index_repr = [indices(n, length) for n in ints]
        print(seq)
        print(binaries)
        print(index_repr)
        print(ints)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("s", type=int)
    parser.add_argument("t", type=int)
    parser.add_argument("mode", choices=["graph", "dfs", "bts"])
    parser.add_argument("start", nargs="?", type=int)
    args = parser.parse_args()
    length = args.s + args.t

    if args.mode == "graph":
        graph = build_graph(args.s, args.t)
        print_graph(graph)

    elif args.mode == "dfs":
        graph = build_graph(args.s, args.t)
        start_node = args.start if args.start is not None else max(graph.keys())
        if start_node not in graph:
            print(f"Ο κόμβος {start_node} δεν υπάρχει στον γράφο.")
            return
        all_paths = []
        dfs(graph, start_node, set(), [], all_paths, len(graph), length)

        if not all_paths:
            print("Δεν βρέθηκε διαδρομή.")
        else:
            for path in all_paths:
                binary_path = [to_binary(n, length) for n in path]
                index_path = [indices(n, length) for n in path]
                print(binary_path)
                print(index_path)
                print(path)

    elif args.mode == "bts":
        bts_mode(args.s, args.t)

if __name__ == "__main__":
    main()