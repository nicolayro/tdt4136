from Map import Map_Obj


# Simple queue implementation
class Queue:
    def __init__(self):
        self.elements = []

    def enqueue(self, element):
        self.elements.append(element)

    def dequeue(self):
        return self.elements.pop(0)

    def is_empty(self):
        return len(self.elements) == 0


def get_neighbors(node):
    pass


def breadth_first_search(graph, start):
    """
    Performs breadth first on graph at given starting point.
    Based on 'Implementation of A*' by Red Blob Games
        https://www.redblobgames.com/pathfinding/a-star/implementation.html
    """

    frontier = Queue()
    frontier.enqueue(start)

    reached = {
        start: True
    }

    while not frontier.is_empty():
        current = frontier.dequeue()
        print(f'  Visiting {current}')

        for next in graph


def a_star():
    pass


def main():
    # Task 1
    my_map = Map_Obj(task=1)
    my_map.show_map()


if __name__ == "__main__":
    main()
