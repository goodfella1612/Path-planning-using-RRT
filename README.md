# RRT algorithm

## Introduction

This repository contains Python code for a RRT algorithm which fins a possibble path between 2 points while avoiding obstacles. Two versions of the code are provided, each with distinct functionality.

### Contents

1. [maze_generator_rrt](#maze_generator_rrt)
2. [random_polygon_rrt](#random_polygon_rrt)

## maze_generator_rrt

### Description

The "maze_generator_rrt.py" script allows users to interactively add barriers to the plot by left-clicking and removing them by right-clicking. The algorithm then finds a path from the bottom left to the top right corner of the plot and shows the path.

### How to Use
1. Download the image provided and change the code to use that image at line 18 by providing the images path.
2. Execute the script using a Python interpreter.
3. Left-click to add a barrier.
4. Right-click to remove a barrier.
5. Observe the path through the barriers\by closing the first plot.

## random_polygon_rrt

### Description

The `random_polygon_rrt.py` script implements thr RRT algorithm within a set of randomly generated non-intersecting polygons. The polygons are generated and the user can interactively add the start and end point of the random path.The algorithm will find a path to the goal point and plot it.

### How to Use

1. Execute the script using a Python interpreter.
2. Left click to add the start point.
3. Right click to add the goal point>
4. do not click within the polygon
5. close the plot window to obtain the path
## Requirements

- Python 3.x
- Required Python packages are specified in the script.
