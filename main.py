import matplotlib.colors as mpl
import matplotlib.pyplot as plt
import networkx as nx
from numpy import inf

# Create a graph with nodes and edges
G = nx.MultiGraph()
f = open("input.txt", "r")
for line in f:
    node1 = int(line.split(" ")[0])
    node2 = int(line.split(" ")[1])
    weight = int(line.split(" ")[2])
    G.add_edge(node1, node2, weight=weight)
f.close()
# 3. Вивести визначення та значення основних характеристик графа (матриця суміжності, інциндентності, хроматичне число та реберне хроматичне число та інші)
print("\nMатриця суміжності\n", nx.adjacency_matrix(G))
print("\nMатриця інциндентносi\n", nx.incidence_matrix(G))
# Compute the chromatic number
graph_coloring = nx.coloring.greedy_color(G)
unique_colors = set(graph_coloring.values())
# Identify edges with different colors
chromatic_edges = [
    (u, v) for u, v in G.edges() if graph_coloring[u] != graph_coloring[v]
]

print(f"\nХроматичне число: {len(unique_colors)}")
# Calculate the maximum degree of the graph
max_degree = max(G.degree, key=lambda x: x[1])[1]

# The edge chromatic number is either max_degree or max_degree + 1
edge_chromatic_number = max_degree if nx.is_eulerian(G) else max_degree + 1

print(f"Реберне хроматичне число: {edge_chromatic_number}")
print(f"\nChromatic edges: {chromatic_edges}")

# 4. Написати програму для знаходження всіх ейлерових ланцюгів та циклів
if nx.is_eulerian(G):
    eulerian_circuit_edges = list(nx.eulerian_circuit(G))
    print("Eulerian circuit edges:", eulerian_circuit_edges)

    eulerian_circuit_vertices = [u for u, v in eulerian_circuit_edges]
    print("Eulerian circuit vertices:", eulerian_circuit_vertices)
else:
    print("\nГраф не є ейлеровим")
    H = nx.eulerize(G)

    eulerian_circuit_edges = list(nx.eulerian_circuit(H))
    print("Eulerian circuit edges:", eulerian_circuit_edges)

    # Get the sequence of vertices in the Eulerian circuit
    eulerian_circuit_vertices = [u for u, v in eulerian_circuit_edges]
    print("Eulerian circuit vertices:", eulerian_circuit_vertices)
if nx.has_eulerian_path(G):
    eulerian_path_edges = list(nx.eulerian_path(G))
    print("Eulerian path edges:", eulerian_path_edges)
else:
    print("The graph does not have an Eulerian path.")
    H = nx.eulerize(G)

    print("Original grahp:")
    print(nx.edges(G))

    print("\nNew eulerian grahp:")
    print(nx.edges(H))

    eulerian_path_edges = list(nx.eulerian_path(H))
    print("Eulerian path edges:", eulerian_path_edges)


# 5. Написати програму для знаходження всіх гамільтонових ланцюгів та циклів
def hamiltonianPaths(G, v, visited, path):
    # if all the vertices are visited, then the Hamiltonian path exists
    if len(path) == len(G.nodes):
        if path[0] in G.neighbors(path[-1]):
            print("Hamiltonian cycle found:", path + [path[0]])
            print("Hamilton graph")
        print(path)
        return

    # Check if every edge starting from vertex `v` leads to a solution or not
    for w in G.neighbors(v):
        if not visited[w]:
            visited[w] = True
            path.append(w)
            hamiltonianPaths(G, w, visited, path)
            visited[w] = False
            path.pop()


def findHamiltonianPaths(G):
    for start in G.nodes:
        path = [start]
        visited = {node: False for node in G.nodes}
        visited[start] = True
        hamiltonianPaths(G, start, visited, path)


n = G.number_of_nodes()

findHamiltonianPaths(G)

# 6. Реалізувати програмно обхід графа пошуком углиб
dfs_edges = list(nx.dfs_edges(G, source=list(G.nodes)[0]))
print("\nобхід графа пошуком углиб:", dfs_edges)

# 7. Реалізувати програмно обхід графа пошуком вшир
dfs_edges = list(nx.bfs_edges(G, source=list(G.nodes)[0]))
print("\nобхід графа пошуком вшир", dfs_edges)


# 8. На мові програмування реалізувани пошук найкородших відстаней на графі від заданої вершини (алгоритм Дейкстри). Вивести схему маршрутів і довжину відстаней.
path = dict(nx.all_pairs_dijkstra_path(G), weight="weight")
print("\nалгоритм Дейкстри:", path)

# 9. На мові програмування реалізувани пошук найкородших відстаней між будь-якими двома вершинами графу (алгоритм Флойда). Вивести схему маршрутів і довжину відстаней.
fw = nx.floyd_warshall(G, weight="weight")
results = {a: dict(b) for a, b in fw.items()}
print("\nалгоритм Флойда:", results)

# 10. Знайти між якою парою вершин найкоротша відстань є найдовшою серед всіх найкоротших відстаней.
# results
max_distance = 0
vertices = ()
for start_node, connections in results.items():
    for end_node, distance in connections.items():
        if distance > max_distance and distance != inf:
            max_distance = distance
            vertices = (start_node, end_node)
print(
    f"\nнайкоротша відстань є найдовшою серед всіх найкоротших відстаней: {vertices}, {max_distance}."
)

# 11. Знайти між якою парою вершин найкоротша відстань є найкоротшою серед всіх найкоротших відстаней.
min_distance = max_distance
for start_node, connections in results.items():
    for end_node, distance in connections.items():
        # NOTE: not including node to itself
        if distance < min_distance and start_node != end_node:
            min_distance = distance
            vertices = (start_node, end_node)
print(
    f"\nнайкоротша відстань є найкоротшою серед всіх найкоротших відстаней: {vertices}, {min_distance}."
)

graph_color_to_mpl_color = dict(zip(unique_colors, mpl.TABLEAU_COLORS))
node_colors = [graph_color_to_mpl_color[graph_coloring[n]] for n in G.nodes()]


pos = nx.spring_layout(G, seed=14)
nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=500,
    node_color=node_colors,
    font_size=12,
    font_color="#333333",
    width=2,
)

plt.show()