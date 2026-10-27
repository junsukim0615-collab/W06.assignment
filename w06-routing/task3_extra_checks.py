"""Additional correctness checks and a like-for-like timing comparison."""
import random
import bench
import task3_reconverge as T


def check_small_graphs():
    count = 0
    for seed in range(20):
        rng = random.Random(seed)
        graph = {str(i): {} for i in range(8)}
        router = T.YourRouter(graph, '0')
        for _ in range(200):
            a, b = rng.sample(list(graph), 2)
            cost = rng.choice([None, 1, 1, 2, 3])
            router.link_change(a, b, cost)
            if cost is None:
                graph[a].pop(b, None)
                graph[b].pop(a, None)
            else:
                graph[a][b] = graph[b][a] = cost
            assert router.table == T.dijkstra_table(graph, '0'), (seed, a, b, cost)
            count += 1
    print(f'PASS: {count} extra events, including disconnected graphs and equal costs')


if __name__ == '__main__':
    check_small_graphs()
    graph, events = bench.build()
    print('Timing both implementations without reference checks:')
    bench.run(T.FullRecompute, 'baseline', graph, events, check=False)
    bench.run(T.YourRouter, 'yours', graph, events, check=False)
