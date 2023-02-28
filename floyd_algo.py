def creation_matrix(edges: list, nodes: list):
    """
    create matrix from edhes and nodes
    >>> creation_matrix([(0, 1, {'weight': 12}), (0, 2, {'weight': 3}), (0, 3, {'weight': -3}),\
    (1, 2, {'weight': 4}), (1, 3, {'weight': -4}), (2, 0, {'weight': 13}),\
    (2, 3, {'weight': 5}), (3, 1, {'weight': -3}), (3, 2, {'weight': 14})],[0, 1, 2, 3])
    [[0, 12, 3, -3], [inf, 0, 4, -4], [13, inf, 0, 5], [inf, -3, 14, 0]]
    """
    matrix_list = []
    for i in range(len(nodes)):
        container = []
        for j in range(len(nodes)):
            if i == j:
                container.append(0)
            else:
                container.append(math.inf)
        matrix_list.append(container)
    for element in edges:
        matrix_list[element[0]][element[1]] = element[2].get("weight")
    return matrix_list


def floyd_algo(matrix_list: list, nodes: list):
    """
    floyd algotithm with using stratred matrix and nodes
            # Distances with 0 source: {0: 0, 1: -6, 2: -2, 3: -10}
    # Distances with 1 source: {0: 10, 1: -7, 2: -3, 3: -11}
    # Distances with 2 source: {0: 13, 1: 2, 2: 0, 3: -2}
    # Distances with 3 source: {0: 7, 1: -10, 2: -6, 3: -14}
    returns new matrix and distances between nodes
    >>> floyd_algo([[0, 12, 3, -3], [math.inf, 0, 4, -4], [13, math.inf, 0, 5], [math.inf, -3, 14, 0]],[0, 1, 2, 3])
    [[0, -6, -2, -10], [10, -7, -3, -11], [13, 2, 0, -2], [7, -10, -6, -14]]
    """
    for node in nodes:
        for i in range(len(matrix_list)):
            for j in range(len(matrix_list)):
                matrix_list[i][j] = min(
                    matrix_list[i][j], matrix_list[i][node] + matrix_list[node][j]
                )
    # for i in nodes:
    #     print(f"Distances with {i} source:", dict(zip(nodes, matrix_list[i])))
    return matrix_list

def timing(values):
    num_of_iterations = 100
    time_w = 0
    nx_time = 0
    list_w = []
    nx_list = []
    for i in range(len(values)):
        print(i)
        G = gnp_random_connected_graph(values[i], 1 , True, False)
        edges = list(G.edges(data=True))
        nodes = list(G.nodes())
        for j in range(num_of_iterations):
            start = time.time()
            floyd_warshall_predecessor_and_distance(G)
            end = time.time()
            nx_time += end - start
            start = time.time()
            floyd_algo(creation_matrix(edges, nodes), nodes)
            end = time.time()
            time_w += end - start
        list_w.append(time_w/num_of_iterations)
        nx_list.append(nx_time/num_of_iterations)
    return list_w, nx_list

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
    values = range(10, 500, 35)
    floyd_times, nx_times = timing(values)
    print(f'Minimal value of written algorithm: {min(floyd_times)}, \
            Maximum value: {max(floyd_times)}')
    print(f'Minimal value of implemented algorithm: {min(nx_times)}, \
            Maximum value: {max(nx_times)}')
    plt.plot(values, floyd_times, label="Written")
    plt.plot(values, nx_times, label="Nx")
    plt.legend()
    plt.xlabel("Graph size")
    plt.ylabel("Time (seconds)")
    plt.show()

