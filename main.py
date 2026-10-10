
import heapq
import networkx as nx
import matplotlib.pyplot as plt

TRAFFIC_WEIGHTS = {
    "Low": 0,
    "Medium": 2,
    "High": 4,
    "Heavy": 6
}

AVERAGE_SPEED_KMPH = 40
FUEL_COST_PER_KM = 5

G = nx.DiGraph()

LOCATIONS = [
    "Home", "College", "Office", "Station",
    "Park", "Airport", "Mall", "Hospital"
]

G.add_nodes_from(LOCATIONS)

# Demonstration road network based on the project concept
ROADS = [
    ("Home", "College", 2, "Low"),
    ("Home", "Park", 6, "Medium"),
    ("Home", "Mall", 4, "High"),
    ("College", "Office", 1, "Low"),
    ("College", "Hospital", 4, "Medium"),
    ("College", "Park", 2, "Low"),
    ("College", "Mall", 4, "Medium"),
    ("College", "Airport", 4, "High"),
    ("Park", "Airport", 8, "Heavy"),
    ("Park", "Office", 10, "Low"),
    ("Mall", "Station", 1, "Medium"),
    ("Mall", "Office", 5, "High"),
    ("Mall", "Hospital", 4, "Medium"),
    ("Station", "Airport", 1, "Low"),
    ("Station", "Office", 2, "Low"),
    ("Hospital", "Airport", 4, "Medium"),
    ("Hospital", "College", 4, "High"),
    ("Airport", "Office", 4, "Low")
]

for source, destination, distance, traffic in ROADS:
    penalty = TRAFFIC_WEIGHTS[traffic]
    G.add_edge(
        source, destination,
        distance=distance,
        traffic=traffic,
        traffic_penalty=penalty,
        cost=distance + penalty
    )


def dijkstra(graph, source, destination):
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}

    distances[source] = 0
    queue = [(0, source)]

    while queue:
        current_cost, current = heapq.heappop(queue)

        if current_cost > distances[current]:
            continue

        if current == destination:
            break

        for neighbor, data in graph[current].items():
            new_cost = current_cost + data["cost"]

            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                previous[neighbor] = current
                heapq.heappush(queue, (new_cost, neighbor))

    if distances[destination] == float("inf"):
        return None, float("inf")

    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = previous[current]

    return path[::-1], distances[destination]


def route_details(graph, path):
    distance = 0
    penalty = 0

    for u, v in zip(path[:-1], path[1:]):
        edge = graph[u][v]
        distance += edge["distance"]
        penalty += edge["traffic_penalty"]

    return distance, penalty


def find_all_routes(graph, source, destination):
    routes = []

    try:
        for path in nx.all_simple_paths(
            graph, source, destination
        ):
            distance, penalty = route_details(graph, path)
            routes.append({
                "path": path,
                "distance": distance,
                "penalty": penalty,
                "cost": distance + penalty
            })
    except nx.NetworkXNoPath:
        pass

    return sorted(routes, key=lambda item: item["cost"])


def display_results(source, destination):
    path, cost = dijkstra(G, source, destination)

    print("\n========== OPTIMAL ROUTE RESULT ==========")
    print("Source:", source)
    print("Destination:", destination)

    if path is None:
        print("No route exists between these locations.")
        return

    distance, penalty = route_details(G, path)
    time_minutes = distance / AVERAGE_SPEED_KMPH * 60
    fuel_cost = distance * FUEL_COST_PER_KM

    print("Optimal route:", " -> ".join(path))
    print("Distance:", distance, "km")
    print("Traffic penalty:", penalty)
    print("Optimized cost:", cost)
    print(f"Estimated travel time: {time_minutes:.1f} minutes")
    print(f"Estimated fuel cost: Rs. {fuel_cost:.2f}")

    print("\nTraffic analysis:")
    for u, v in zip(path[:-1], path[1:]):
        print(f"{u} -> {v}: {G[u][v]['traffic']} traffic")

    print("\n========== ALTERNATIVE ROUTES ==========")
    for i, route in enumerate(
        find_all_routes(G, source, destination), start=1
    ):
        print(
            f"Route {i}: {' -> '.join(route['path'])} | "
            f"Distance: {route['distance']} km | "
            f"Cost: {route['cost']}"
        )


def visualize_graph(source, destination):
    path, _ = dijkstra(G, source, destination)

    positions = {
        "Home": (0, 1),
        "Park": (1, 2),
        "College": (2, 0.5),
        "Hospital": (3, -0.5),
        "Airport": (4, 1.5),
        "Station": (5, 2.5),
        "Mall": (5, 0.5),
        "Office": (7, 2)
    }

    plt.figure(figsize=(12, 7))

    colors = [
        "green" if node == source else
        "orange" if node == destination else
        "skyblue"
        for node in G.nodes
    ]

    nx.draw_networkx(
        G, positions,
        node_color=colors,
        node_size=1800,
        font_size=9,
        arrows=True,
        arrowsize=15
    )

    labels = {
        (u, v): f"{data['distance']} km ({data['traffic']})"
        for u, v, data in G.edges(data=True)
    }

    nx.draw_networkx_edge_labels(
        G, positions, edge_labels=labels, font_size=7
    )

    if path and len(path) > 1:
        nx.draw_networkx_edges(
            G, positions,
            edgelist=list(zip(path[:-1], path[1:])),
            edge_color="red",
            width=3,
            arrows=True,
            arrowsize=20
        )

    plt.title(f"Smart Route Optimizer: {source} to {destination}")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def main():
    print("SMART ROUTE OPTIMIZER USING DIJKSTRA'S ALGORITHM")
    print("Available locations:", ", ".join(LOCATIONS))

    source = input("Enter source location: ").strip().title()
    destination = input("Enter destination location: ").strip().title()

    if source not in G or destination not in G:
        print("Invalid location. Use a name from the available list.")
        return

    if source == destination:
        print("Source and destination are the same. Distance: 0 km")
        return

    display_results(source, destination)
    visualize_graph(source, destination)


if __name__ == "__main__":
    main()

