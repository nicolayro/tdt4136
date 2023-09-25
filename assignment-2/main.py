from Map import Map_Obj
import queue


def get_neighbors(graph, node):
    neighbors = []
    [x, y] = node

    if x > 0:
        neighbors.append([x - 1, y]),
    if y > 0:
        neighbors.append([x, y - 1]),
    if x < len(graph):
        neighbors.append([x + 1, y])
    if y < len(graph[0]):
        neighbors.append([x, y + 1]),

    return [n for n in neighbors if graph[n[0]][n[1]] >= 0]


def heuristic(a, b):
    [x1, y1] = a
    [x2, y2] = b

    return abs(x1-x2) + abs(y1-y2)


def a_star(graph, start, goal):
    """
    Performs breadth first on graph at given starting point.
    Based on 'Implementation of A*' by Red Blob Games
        https://www.redblobgames.com/pathfinding/a-star/implementation.html
    """

    frontier = queue.PriorityQueue()
    frontier.put((start, 0))

    came_from = {tuple(start): None}
    cost_so_far = {tuple(start): 0}

    while not frontier.empty():
        current = frontier.get()[0]

        if current == goal:
            break

        for next in get_neighbors(graph, current):
            next_cost = graph[next[0]][next[1]]
            new_cost = cost_so_far[tuple(current)] + next_cost
            #if tuple(next) not in cost_so_far or new_cost < cost_so_far[tuple(next)]:
            if new_cost < cost_so_far.get(tuple(next), 1_000_000):
                cost_so_far[tuple(next)] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put((next, priority))
                came_from[tuple(next)] = current

    return came_from


def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[tuple(current)]
    path.reverse()
    return path


def visualize_result(m, result):
    for pos in result:
        if pos != m.get_goal_pos():
            m.set_cell_value(pos, 10)
    m.show_map()


def main():
    # Task 1

    for i in range(5):
        # Intialize map for each task
        m = Map_Obj(task=i + 1)

        # Perform search and vizualise shortest path
        result = a_star(m.int_map, m.get_start_pos(), m.get_goal_pos())
        path = reconstruct_path(result, m.get_start_pos(), m.get_goal_pos())
        visualize_result(m, path)


if __name__ == "__main__":
    main()
