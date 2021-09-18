# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains search functions.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (alpha, beta, gamma) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs)
# You may need to slight change your previous search functions in MP1 since this is 3-d maze

from collections import deque
from heapq import heappop, heappush

def search(maze, searchMethod):
    return {
        "bfs": bfs,
    }.get(searchMethod, [])(maze)

def bfs(maze, ispart1=True):
    #print(maze.levels)
    q = deque()
    path = deque()
    parentdict ={}
    visited = set()
    #print(maze)
    start = maze.getStart()
    #shape = start[2]
    print(start)
    q.append(start)
    visited.add(start)
    #print(maze.waypoints)
    while len(q) != 0:
        currentpoint = q.popleft()
        #print(startpoint)
        if maze.isObjective(currentpoint[0],currentpoint[1],currentpoint[2],ispart1) == True:
            path.appendleft(currentpoint)
            while path[0] != start:
                path.appendleft(parentdict[currentpoint])
                currentpoint = parentdict[currentpoint]
            return path

        for neighbor in maze.getNeighbors(currentpoint[0],currentpoint[1],currentpoint[2],ispart1):
            if neighbor not in visited:
                parentdict[neighbor] = currentpoint
                q.append(neighbor)
                visited.add(neighbor)

   # return []
 