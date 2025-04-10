import argparse
from itertools import permutations

# Βοηθητική: Από δυαδική συμβολοσειρά -> δείκτες μονάδων
def binary_string_to_indices(s):
    return [i for i, ch in enumerate(s) if ch == '1']

# Απόσταση Hamming μεταξύ λιστών δεικτών
def hamming_distance_indices(a, b):
    return sum(x != y for x, y in zip(a, b))

# Έλεγχος genlex μεταξύ διαδοχικών κόμβων
def is_genlex(path, next_node):
    print(f"Έλεγχος genlex για το μονοπάτι: {path} με τον κόμβο {next_node}")
   
    # Ελέγχει αν το μονοπάτι παραμένει genlex όταν προσθέσουμε τον κόμβο.
    def indices(n):
        return [i for i, bit in enumerate(format(n, f'0{path[0].bit_length()}b')) if bit == '1']
    
    for i in range(1, len(path) + 1):
        if indices(path[-i])[:i] != indices(next_node)[:i]:
            print(f"Δεν πληρείται genlex για {path[-i]} και {next_node}")
            return False
    return True

# Αναδρομική DFS
def dfs(graph, current, visited, path, all_paths, total_nodes):
    print(f"Αναδρομή: τρέχων κόμβος = {current}, διαδρομή = {path}")
    visited.add(current)
    path.append(current)

    # Όταν βρεθεί μια πλήρης διαδρομή
    if len(path) == total_nodes:
        all_paths.append(list(path))
        print(f"Βρέθηκε διαδρομή: {path}")
    else:
        for neighbor in graph[current]:
            current_bin = format(current, f'0{path[0].bit_length()}b')
            neighbor_bin = format(neighbor, f'0{path[0].bit_length()}b')

            # Υπολογισμός απόστασης Hamming
            hamming_dist = hamming_distance_indices(binary_string_to_indices(current_bin), binary_string_to_indices(neighbor_bin))
            print(f"Απόσταση Hamming μεταξύ {current} και {neighbor}: {hamming_dist}")

            if neighbor not in visited and hamming_dist == 2:
                print(f"Καλείται αναδρομικά με {neighbor}")
                # Ελέγχουμε αν πληρούται η γενική λεξιγραφική σειρά
                if is_genlex(path, neighbor):
                    dfs(graph, neighbor, visited, path, all_paths, total_nodes)

    visited.remove(current)
    path.pop()
    print(f"Επιστροφή από {current}, τρέχουσα διαδρομή = {path}")

# Δημιουργία κόμβων ως δυαδικές συμβολοσειρές και δεκαδικοί
def generate_nodes(s, t):
    perms = set(permutations('0' * s + '1' * t))
    bin_nodes = [''.join(p) for p in perms]
    unique_bin_nodes = sorted(set(bin_nodes))
    decimal_nodes = [int(b, 2) for b in unique_bin_nodes]
    return unique_bin_nodes, decimal_nodes

# Κατασκευή γράφου μεταθέσεων
def build_graph(s, t):
    bin_nodes, dec_nodes = generate_nodes(s, t)
    graph = {n: [] for n in dec_nodes}
    for i in range(len(bin_nodes)):
        for j in range(i + 1, len(bin_nodes)):
            a, b = bin_nodes[i], bin_nodes[j]
            if sum(x != y for x, y in zip(a, b)) == 2:  # Απόσταση Hamming = 2
                if sorted(a) == sorted(b):  # Η τάξη των μηδενικών και μονάδων είναι η ίδια
                    a_dec = int(a, 2)
                    b_dec = int(b, 2)
                    graph[a_dec].append(b_dec)
                    graph[b_dec].append(a_dec)
    return graph, bin_nodes, dec_nodes

# DFS handler
def handle_dfs(s, t, start_node=None):
    print(f"Εκτελείται η συνάρτηση handle_dfs με s={s}, t={t}, start_node={start_node}")
    graph, bin_nodes, dec_nodes = build_graph(s, t)
    indices_map = {int(b, 2): binary_string_to_indices(b) for b in bin_nodes}
    all_paths = []

    start_nodes = [start_node] if start_node is not None else dec_nodes
    for start in start_nodes:
        visited = set()
        path = []
        dfs(graph, start, visited, path, all_paths, len(dec_nodes))

    # Εκτύπωση των διαδρομών
    for path in all_paths:
        binary_path = [format(n, f'0{s + t}b') for n in path]
        indices_path = [binary_string_to_indices(b) for b in binary_path]
        print(f"Διαδρομή (Δυαδικά): {binary_path}")
        print(f"Δείκτες: {indices_path}")
        print(f"Ακέραιοι: {path}")

# Main πρόγραμμα
print("Το πρόγραμμα εκκινεί...")
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
input("Πατήστε Enter για να κλείσετε το πρόγραμμα...")
