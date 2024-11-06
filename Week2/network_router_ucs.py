import heapq


def network_router_ucs(networks, start_router, goal_router):
    priority_queue = [(0, start_router, [])]  # stores [(cost , current_node , path)]
    visited = set()

    while priority_queue:
        current_cost, current_router, current_path = heapq.heappop(priority_queue)

        if current_router == goal_router:
            return current_path + [current_router], current_cost

        if current_router in visited:
            continue  # skips the current iteration

        visited.add(current_router)

        for neighbor, link_cost in networks.get(current_router):
            if neighbor not in visited:
                total_cost = current_cost + link_cost  # adding up the costs
                heapq.heappush(priority_queue, (total_cost, neighbor, current_path + [current_router]))
                # selection of router is through least total_cost after adding up the link_cost

    return None, float('inf')


network = {
    "Router1": [("Router2", 10), ("Router3", 15)],
    'Router2': [('Router1', 10), ('Router4', 12), ('Router3', 5)],
    'Router3': [('Router1', 15), ('Router2', 5), ('Router5', 10)],
    'Router4': [('Router2', 12), ('Router5', 2)],
    'Router5': [('Router3', 10), ('Router4', 2)]
}

path, final_cost = network_router_ucs(network, "Router1", "Router5")

if path:
    print(f"path found is {path} and \nCost for the found path is {final_cost}")
else:
    print("No path found")
