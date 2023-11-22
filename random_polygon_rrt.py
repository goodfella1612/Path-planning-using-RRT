from shapely.geometry import Polygon, Point, LineString
import random
import matplotlib.pyplot as plt
import math

fig, ax = plt.subplots()
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
nodes = []
node_pair = []
right_click_triggered = False


def create_polygon():
    # Function to create a valid polygon with a random number of sides
    while True:
        sides = random.randint(3, 13)
        coords = []
        for _ in range(sides):
            x = random.uniform(0, 100)
            y = random.uniform(0, 100)
            coords.append((x, y))
        polygon = Polygon(coords)
        if polygon.is_valid:
            break
    return polygon


def generate_polygons(n):
    # Function to generate a list of non-intersecting polygons
    polygons_list = []
    for _ in range(n):
        while True:
            new_polygon = create_polygon()
            intersects = any(new_polygon.intersects(existing_polygon) for existing_polygon in polygons_list)
            if not intersects:
                polygons_list.append(new_polygon)
                break
    return polygons_list


def display_polygons(polygons_list):
    # Function to display polygons
    for polygon in polygons_list:
        x, y = polygon.exterior.xy
        plt.plot(x, y)
    plt.show()


def show_polygon(polygons_list):
    # Function to display polygons without clearing the plot
    for polygon in polygons_list:
        x, y = polygon.exterior.xy
        plt.plot(x, y)


def on_click(event):
    global right_click_triggered
    if event.button == 1:  # Left mouse button (create circle)
        c1 = event.xdata
        c2 = event.ydata
        print((c1, c2))
        center = Point(c1, c2)
        nodes.append(center)
        circle = center.buffer(1)
        x, y = circle.exterior.xy
        plt.plot(x, y, color='blue')
        plt.show()
    elif event.button == 3:  # Right mouse button (create circle)
        c1 = event.xdata
        c2 = event.ydata
        print((c1, c2))
        center = Point(c1, c2)
        circle = center.buffer(1)
        nodes.append(center)
        x, y = circle.exterior.xy
        plt.plot(x, y, color='red')
        plt.show()
        right_click_triggered = True


def create_random_node():
    # Function to create a random node within the plot boundaries
    x = random.uniform(0, 100)
    y = random.uniform(0, 100)
    return Point(x, y)


def find_nearest_node(current_node):
    # Function to find the nearest node to a given point
    minimum_distance = math.inf
    for node in nodes:
        distance = current_node.distance(node)
        if distance < minimum_distance:
            minimum_distance = distance
            nearest_node = node
    return minimum_distance, nearest_node


def modify_node(current_node, nearest, polygons_list):
    # Function to modify a node's position towards another node while avoiding polygons
    step = 15
    direction = Point(current_node.x - nearest[1].x, current_node.y - nearest[1].y)
    if nearest[0] > step:
        direction = Point(direction.x * step / nearest[0], direction.y * step / nearest[0])
    new_point = Point(direction.x + nearest[1].x, direction.y + nearest[1].y)
    line = LineString([new_point, nearest[1]])
    for polygon in polygons_list:
        if polygon.intersects(line):
            return 0
    return new_point

def calculate_distance(point1, point2):
    # Function to calculate the distance between two points
    return point1.distance(point2)

def main(num_polygons):
    polygons_list = generate_polygons(num_polygons)
    display_polygons(polygons_list)
    goal_point = nodes.pop()

    for _ in range(2000):
        new_node = create_random_node()
        nearest_node_info = find_nearest_node(new_node)
        modified_node = modify_node(new_node, nearest_node_info, polygons_list)

        if modified_node == 0:
            continue

        nodes.append(modified_node)
        node_pair.append((nearest_node_info[1], modified_node))
        plt.plot([modified_node.x, nearest_node_info[1].x], [modified_node.y, nearest_node_info[1].y], c='blue')
        x, y = modified_node.xy
        plt.plot(x, y, 'bo')

        if calculate_distance(modified_node, goal_point) < 15:
            plt.plot([modified_node.x, goal_point.x], [modified_node.y, goal_point.y], c='red')
            print('Success')
            break

    final_node = nodes[-1]
    while True:
        for pair in node_pair:
            if pair[1] == final_node:
                plt.plot([final_node.x, pair[0].x], [final_node.y, pair[0].y], c="yellow")
                x, y = pair[0].xy
                plt.plot(x, y, 'yo')
                final_node = pair[0]
                break
        if final_node == nodes[0]:
            break

    x, y = goal_point.xy
    plt.plot(x, y, 'ro')  # plots goal point
    start_node = nodes[0]
    x, y = start_node.xy
    plt.plot(x, y, 'go')  # plots start point
    show_polygon(polygons_list)
    plt.show()


fig.canvas.mpl_connect('button_press_event', on_click)
main(4)
