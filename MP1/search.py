# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Kelvin Ma (kelvinm2@illinois.edu) on 01/24/2021

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,fast)


# Feel free to use the code below as you wish
# Initialize it with a list/tuple of objectives
# Call compute_mst_weight to get the weight of the MST with those objectives
# TODO: hint, you probably want to cache the MST value for sets of objectives you've already computed...
from collections import deque
import heapq

class MST:
    def __init__(self, objectives):
        self.elements = {key: None for key in objectives}

        # TODO: implement some distance between two objectives 
        # ... either compute the shortest path between them, or just use the manhattan distance between the objectives
        def DISTANCE(point1, point2):
            return abs(point1[0]-point2[0])+abs(point1[1]-point2[1])
        self.distances   = {
                (i, j): DISTANCE(i, j)
                for i, j in self.cross(objectives)
            }
        
    # Prim's algorithm adds edges to the MST in sorted order as long as they don't create a cycle
    def compute_mst_weight(self):
        weight      = 0
        for distance, i, j in sorted((self.distances[(i, j)], i, j) for (i, j) in self.distances):
            if self.unify(i, j):
                weight += distance
        return weight

    # helper checks the root of a node, in the process flatten the path to the root
    def resolve(self, key):
        path = []
        root = key 
        while self.elements[root] is not None:
            path.append(root)
            root = self.elements[root]
        for key in path:
            self.elements[key] = root
        return root
    
    # helper checks if the two elements have the same root they are part of the same tree
    # otherwise set the root of one to the other, connecting the trees
    def unify(self, a, b):
        ra = self.resolve(a) 
        rb = self.resolve(b)
        if ra == rb:
            return False 
        else:
            self.elements[rb] = ra
            return True

    # helper that gets all pairs i,j for a list of keys
    def cross(self, keys):
        return (x for y in (((i, j) for j in keys if i < j) for i in keys) for x in y)

def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """

    q = deque()
    path = deque()
    parentdict ={}
    visited = set()
    q.append(maze.start)
    #print(maze.waypoints)
    while len(q) != 0:
        startpoint = q.popleft()
        #print(startpoint)
        if startpoint not in visited:
            visited.add(startpoint)
            #print("visited is" )
            #print(visited)
            for point in maze.neighbors(startpoint[0],startpoint[1]):
                if point not in visited:
                    parentdict[point] = startpoint  # keep track of the parent of visited node
                    #print(maze.states_explored)
                #print(parentdict[point])

                    if point == maze.waypoints[0]:  #found waypoint, find the path now
                        #print (numberofstep)
                        #print (parentdict)
                        while point != maze.start:
                           
                            path.appendleft(point)
                            #print(point)

                            point = parentdict[point] # back track parent node for the path
                           
                            
                        #print("path is")
                        #print(path)
                        path.appendleft(maze.start)
                        return path
                    else:
                        q.append(point) #add neighbor to frontier queue
                        #print(q)
                
    return []

def h_single(point1, point2):

    return abs(point1[0]-point2[0])+abs(point1[1]-point2[1])

def h_multiple(current_pos, remaining_goals):

    closest_goal = None
    dis = 99999
    for goal in remaining_goals:
        if h_single(goal,current_pos) < dis:
            closest_goal = goal
            dis =  h_single(goal,current_pos)
    mst = MST(remaining_goals)
    h_total = dis + mst.compute_mst_weight()

    return h_total

def astar_single(maze):
    """
    Runs A star for part 2 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    q = []
    heapq.heapify(q)
    path = deque()
    parentdict = {}
    depthdict ={} #keep track of g(a)
    visited = set()
    depthdict[maze.start] = 0
    heapq.heappush(q,(depthdict[maze.start]+h_single(maze.start,maze.waypoints[0]),maze.start))
    #print(q)
    while len(q) != 0:
        startpoint = heapq.heappop(q)[1]
        #print(startpoint)
        if startpoint not in visited:
            visited.add(startpoint)
            #print("visited is" )
            #print(visited)
            for point in maze.neighbors(startpoint[0],startpoint[1]):
                #print(point)
                if point not in visited:
                    parentdict[point] = startpoint  # keep track of the parent of visited node
                    depthdict[point] = depthdict[parentdict[point]] +1
                    #print(maze.states_explored)
                    #print(parentdict[point])

                    if point == maze.waypoints[0]:  #found waypoint, find the path now
                        #print (numberofstep)
                        #print (parentdict)
                        while point != maze.start:
                           
                            path.appendleft(point)
                            #print(point)

                            point = parentdict[point] # back track parent node for the path
                           
                            
                        #print("path is")
                        #print(path)
                        path.appendleft(maze.start)
                        return path
                    else:
                        heapq.heappush(q,(depthdict[point]+h_single(point,maze.waypoints[0]),point)) #add neighbor to heapq
                        #print(q)
                
    return []



#def astar_multiple(maze):
    """
    Runs A star for part 4 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    q = []
    heapq.heapify(q)
    path = deque()
    parentdict = {}
    depthdict ={} #keep track of g(a)
    #remaining_goal_dict = {} #keep track of remaining goal of each state
    visited = set()
    depthdict[maze.start] = 0
    remaining_goal = set(maze.waypoints)
    print(remaining_goal)
    #remaining_goal.remove(maze.waypoints[0])
    #print(remaining_goal)
    print("H_multiple_test")
    print(h_multiple(maze.start,remaining_goal))

    heapq.heappush(q,(depthdict[maze.start]+h_multiple(maze.start,remaining_goal),maze.start))
    #print(q)
    while len(q) != 0:
        startpoint = heapq.heappop(q)[1]
        #print(startpoint)
        if startpoint not in visited:
            visited.add(startpoint)
            #print("visited is" )
            #print(visited)
            for point in maze.neighbors(startpoint[0],startpoint[1]):
                #print(point)
                if point not in visited:
                    parentdict[point] = startpoint  # keep track of the parent of visited node
                    depthdict[point] = depthdict[parentdict[point]] +1
                    #print(maze.states_explored)
                    #print(parentdict[point])

                    if point in remaining_goal:  #found waypoint, find the path now
                        #print (numberofstep)
                        #print (parentdict)
                        while point != maze.start:
                           
                            path.appendleft(point)
                            #print(point)

                            point = parentdict[point] # back track parent node for the path
                           
                            
                        #print("path is")
                        #print(path)
                        path.appendleft(maze.start)
                        return path
                    else:
                        heapq.heappush(q,(depthdict[point]+h_single(point,maze.waypoints[0]),point)) #add neighbor to heapq
                        #print(q)
                
    return []

def astar_multiple(maze):
    """
    Runs A star for part 4 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    
    path = deque()
    path.append(maze.start)
    
    #remaining_goal_dict = {} #keep track of remaining goal of each state
    
    remaining_goal = set(maze.waypoints)
    print(remaining_goal)
    #remaining_goal.remove(maze.waypoints[0])
    #print(remaining_goal)
    #print("H_multiple_test")
    #print(h_multiple(maze.start,remaining_goal))

    #heapq.heappush(q,(depthdict[maze.start]+h_multiple(maze.start,remaining_goal),maze.start))
    #print(q)
    q = []
    heapq.heapify(q)
    visited = set()
    parentdict = {}
    start = maze.start
    depthdict ={} #keep track of g(a)
    depthdict[start] = 0
    heapq.heappush(q,[depthdict[start]+h_multiple(start,remaining_goal),start])
    n = 0
    while len(remaining_goal) != 0:
        print(remaining_goal)
        for item in q:
            item[0] =depthdict[item[1]]+h_multiple(item[1],remaining_goal)
        flag = 0
        #print(maze.neighbors(maze.start[0],maze.start[1]))
        #return 0
        #while len(q) != 0:
        #if flag:
         #   break
        if len(q) ==0:
            visitedlist = list(visited)
            #print(visitedlist)
            q2 = []
            heapq.heapify(q2)
            for item in visitedlist:
                heapq.heappush(q2,[depthdict[item]+h_multiple(item,remaining_goal),item])

            print("q2 is",q2)

            start = heapq.heappop(q2)[1]
            #print("start is",start)

            heapq.heappush(q,[depthdict[start]+h_multiple(start,remaining_goal),start])
            
        startpoint = heapq.heappop(q)[1]
        #print(startpoint)
        if startpoint not in visited:
            visited.add(startpoint)
            print("visited is" )
            print(visited)
            for point in maze.neighbors(startpoint[0],startpoint[1]):
                #if flag:
                    #break
                
                
                if point not in visited:
                    #heapq.heappush(q,[depthdict[point]+h_multiple(point,remaining_goal),point]) #add neighbor to heapq

                    parentdict[point] = startpoint  # keep track of the parent of visited node
                    depthdict[point] = depthdict[parentdict[point]] +1
                    #print(maze.states_explored)
                    #print(parentdict[point])
                    heapq.heappush(q,[depthdict[point]+h_multiple(point,remaining_goal),point]) #add neighbor to heapq

                    if point in remaining_goal:  #found waypoint, find the path now
                        #print (numberofstep)
                        #print (parentdict)
                        
                        remaining_goal.remove(point)
                        while point not in path:
                        
                            path.appendleft(point)
                            print("path is ", path)

                            point = parentdict[point] # back track parent node for the path
                        
                        flag = 1 
                        #print("path is")
                        #print(path)
                        #path.appendleft(start)
                        #return path
                    #else:
                       # heapq.heappush(q,[depthdict[point]+h_multiple(point,remaining_goal),point]) #add neighbor to heapq
                        #print(q)
                    
                
    return path

def fast(maze):
    """
    Runs suboptimal search algorithm for part 5.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    return []
    
            
