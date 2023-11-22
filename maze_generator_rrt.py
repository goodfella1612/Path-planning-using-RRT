import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
from shapely import Polygon, Point, LineString
import random
import math

fig, ax = plt.subplots(figsize=(7, 7))
bpos = []   # List to store barrier positions
lis = []    # List to store barrier annotations
g = []      # List to store Shapely Polygon objects representing barriers
nodes = []  # List to store random nodes
node_pair = []  # List to store pairs of connected nodes


def create_barrier(p1, p2):
    # Function to create a barrier and add it to the plot
    img = mpimg.imread(r'C:\Users\devth\Downloads\x-png-35415.png')
    imagebox = OffsetImage(img, zoom=0.05)
    ab = AnnotationBbox(imagebox, (p1 + 0.5, p2 + 0.5), frameon=False)
    ax.add_artist(ab)
    fig.canvas.draw_idle()
    lis.append(ab)


def destroy_barrier(p1, p2):
    # Function to destroy a barrier based on its position
    for barrier_pos in bpos:
        if barrier_pos == (p1, p2):
            index_to_remove = bpos.index(barrier_pos)
            bpos.remove(barrier_pos)
            barrier_out = lis.pop(index_to_remove)
            barrier_out.remove()
            plt.show()


def on_click(event):
    # Event handler for mouse clicks
    if event.button == 1:  # Left mouse button (create barrier)
        c1 = round(event.xdata)
        c2 = round(event.ydata)
        if (c1, c2) in bpos:
            print('you clicked twice')
        else:
            bpos.append((c1, c2))
            create_barrier(c1, c2)
            print(f'You clicked at ({c1, c2})')
    elif event.button == 3:  # Right mouse button (destroy barrier)
        c1 = round(event.xdata)
        c2 = round(event.ydata)
        destroy_barrier(c1, c2)


fig.canvas.mpl_connect('button_press_event', on_click)

# Plotting the grid
x = [j for i in range(12) for j in range(12)]
y = [i for i in range(12) for _ in range(12)]
ax.scatter(x, y, c='blue', s=0.1)

# Plotting arrows
ax.arrow(0, 0.5, 0.5, 0, fc='green', head_width=0.5, head_length=0.2)
ax.arrow(10, 10.5, 0.5, 0, fc='green', head_width=0.5, head_length=0.2)

ax.set_xlim(0, 11)
ax.set_ylim(0, 11)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_title('whee')

plt.show()


def create_node(polygon_list):
    # Function to create a random node not within any polygon
    while True:
        x = random.uniform(0, 11)
        y = random.uniform(0, 11)
        point = Point(x, y)  # Changed variable name for clarity
        is_within_polygon = any(polygon.contains(point) for polygon in polygon_list)
        if not is_within_polygon:
            nodes.append(point)
            break


def calculate_distance(point1, point2):
    # Function to calculate the Euclidean distance between two points
    return point1.distance(point2)


def nearest_node(a):
    # Function to find the nearest node to a given point
    minimum_dist = math.inf
    for point in nodes:
        distance = calculate_distance(a, point)
        if distance < minimum_dist:
            minimum_dist = distance
            near_point = point
    return minimum_dist, near_point


def modify_node(a, l, polygon_list):
    # Function to modify a node's position towards another node while avoiding obstacles
    step = 1
    direction = Point(a.x - l[1].x, a.y - l[1].y)
    if l[0] > step:
        direction = Point(direction.x * step / l[0], direction.y * step / l[0])
    new_point = Point(direction.x + l[1].x, direction.y + l[1].y)
    line = LineString([new_point, l[1]])
    for polygon in polygon_list:
        if polygon.intersects(line):
            return 0
    return new_point


for barrier_pos in bpos:
    # Creating Shapely Polygon objects representing barriers
    polygon = Polygon([Point(barrier_pos[0], barrier_pos[1]),
                       Point(barrier_pos[0] + 1, barrier_pos[1]),
                       Point(barrier_pos[0] + 1, barrier_pos[1] + 1),
                       Point(barrier_pos[0], barrier_pos[1] + 1)])
    g.append(polygon)
    x, y = polygon.exterior.xy
    plt.plot(x, y)

goal_point = Point(10.5, 10.5)
start_point = Point(0.5, 0.5)
nodes.append(start_point)

for i in range(2500):
    create_node(g)
    a = nodes.pop()
    l = nearest_node(a)
    new_node = modify_node(a, l, g)
    if new_node == 0:
        continue
    nodes.append(new_node)
    node_pair.append((l[1], new_node))
    plt.plot([new_node.x, l[1].x], [new_node.y, l[1].y], c='blue')
    x, y = new_node.xy
    plt.plot(x, y, 'bo')
    if calculate_distance(new_node, goal_point) < 1:
        plt.plot([new_node.x, goal_point.x], [new_node.y, goal_point.y], c='red')
        print('success')
        print(i)
        break

node_pair.append((nodes[-1], goal_point))
o = nodes[-1]
while True:
    for r in node_pair:
        if r[1] == o:
            plt.plot([o.x, r[0].x], [o.y, r[0].y], c="yellow")
            x, y = r[0].xy
            plt.plot(x, y, 'yo')
            o = r[0]
            break
    if o == nodes[0]:
        break

x, y = goal_point.xy
plt.plot(x, y, 'ro')  # plots goal point
b = nodes[0]
x, y = b.xy
plt.plot(x, y, 'go')  # plots start point
plt.show()
