# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by James Gao (jamesjg2@illinois.edu) on 9/03/2021
# Inspired by work done by Jongdeog Lee (jlee700@illinois.edu)

"""
This file contains geometry functions necessary for solving problems in MP2
"""

import math
import numpy as np
from numpy.lib.index_tricks import r_
from alien import Alien



def does_alien_touch_wall(alien, walls,granularity):

    """Determine whether the alien touches a wall

        Args:
            alien (Alien): Instance of Alien class that will be navigating our map
            walls (list): List of endpoints of line segments that comprise the walls in the maze in the format [(startx, starty, endx, endx), ...]
            granularity (int): The granularity of the map

        Return:
            True if touched, False if not
    """
 #   print(walls)
    def wall_intercept_circle(alien, walls,granularity):
        center = alien.get_centroid()
        r = alien.get_width()
       # print(r)
        #print("center is ",center)
        #print(walls)
        #print('stucked')
    
        
        for wall in walls:
        #print(wall)
            #print('current wall is ',wall)
            #print(r)
            #print(center)
            if (wall[2]-wall[0]) != 0: #not vertical line
                slope = (wall[3]-wall[1])/(wall[2]-wall[0])
                #print(slope)
                intercept = wall[1]-slope*wall[0]
                #print(intercept)
                dist_center_to_line = abs(slope*center[0]-center[1]+intercept)/np.sqrt(slope**2+1)
                #print(dist_center_to_line)
                if (dist_center_to_line < r+granularity/np.sqrt(2)) or np.isclose(dist_center_to_line , r+granularity/np.sqrt(2)):
                    min_dist_x_pos = (-1*(-1*center[0]-slope*center[1])-slope*intercept)/(slope**2+1)
                    if (min_dist_x_pos <= max(wall[2], wall[0])) & (min_dist_x_pos >= min(wall[2], wall[0])):
                        return True
                    
            else:  # vertical line   
               # print("shit, vertical line",wall) 
                dist_center_to_line = abs(center[0]-wall[0])
                #print(dist_center_to_line)
                #print(r+granularity/np.sqrt(2))
                if (dist_center_to_line < r+granularity/np.sqrt(2)) or np.isclose(dist_center_to_line , r+granularity/np.sqrt(2)):
                    min_dist_y_pos = center[1]
                    #print('mindist y pos is',min_dist_y_pos)
                    if (min_dist_y_pos < max(wall[3], wall[1])) & (min_dist_y_pos > min(wall[3], wall[1])):
                        return True
                else:
                    #print('min_dist y pos is not in line')
                    continue
                    
        return False 

    def wall_intercept_horizonal(alien, walls,granularity):
        #print("now in horizontal")
        center = alien.get_centroid()
        width = alien.get_width()
        head = alien.get_head_and_tail()[0]
        tail = alien.get_head_and_tail()[1]
        #print(width)
        #print(center)
        #print(head,tail)

        class Point:
            def __init__(self,x,y):
                self.x = x
                self.y = y

        def ccw(A,B,C):
            return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)

        def intersect(A,B,C,D):
            return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

            
        a = Point(head[0]+width,head[1]-width)#bot right
        b = Point(head[0]+width,head[1]+width)#top right
        c = Point(tail[0]-width,tail[1]-width)# bot left
        d = Point(tail[0]-width,tail[1]+width)#top left
        #print(a.x,a.y,b.x,b.y,c.x,c.y,d.x,d.y)
        for wall in walls:
            #print(wall)
            wallPoint_1 = Point(wall[0],wall[1])
            wallPoint_2 = Point(wall[2],wall[3])
            #print(intersect(a,b,wallPoint_1,wallPoint_2))
            #print(intersect(b,c,wallPoint_1,wallPoint_2))
            #print(intersect(c,d,wallPoint_1,wallPoint_2))
            #print(intersect(d,a,wallPoint_1,wallPoint_2))        
            #print(np.isclose(c.x,0) , np.isclose(c.y,0) , np.isclose(b.x,window[0]) , np.isclose(b.y,window[1]))   
            
            if intersect(a,b,wallPoint_1,wallPoint_2) or  intersect(b,c,wallPoint_1,wallPoint_2) or  intersect(c,d,wallPoint_1,wallPoint_2) or intersect(d,a,wallPoint_1,wallPoint_2):
                return True
            
        return False

    def wall_intercept_vertical(alien, walls,granularity):
        #print("now in vertical")
        center = alien.get_centroid()
        width = alien.get_width()
        head = alien.get_head_and_tail()[0]
        tail = alien.get_head_and_tail()[1]
       # #print(width)
       # #print(center)
        #print(head,tail)


        class Point:
            def __init__(self,x,y):
                self.x = x
                self.y = y

        def ccw(A,B,C):
            return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)

        def intersect(A,B,C,D):
            return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)    


        a = Point(head[0]-width,head[1]-width)#bot left
        b = Point(head[0]+width,head[1]-width)#bot right
        c = Point(tail[0]-width,tail[1]+width)# top left
        d = Point(tail[0]+width,tail[1]+width)#top right
        #print(a.x,a.y,b.x,b.y,c.x,c.y,d.x,d.y)
        for wall in walls:
        #print(wall)
            wallPoint_1 = Point(wall[0],wall[1])
            wallPoint_2 = Point(wall[2],wall[3])
            #print(intersect(a,b,wallPoint_1,wallPoint_2))
            #print(intersect(b,c,wallPoint_1,wallPoint_2))
            #print(intersect(c,d,wallPoint_1,wallPoint_2))
            #print(intersect(d,a,wallPoint_1,wallPoint_2))            
            
            if intersect(a,b,wallPoint_1,wallPoint_2) or  intersect(b,c,wallPoint_1,wallPoint_2) or  intersect(c,d,wallPoint_1,wallPoint_2) or intersect(d,a,wallPoint_1,wallPoint_2):
                return True
                
        return False

    if alien.get_shape() == "Ball":
        return wall_intercept_circle(alien, walls,granularity)
    elif alien.get_shape() == "Horizontal":
        return wall_intercept_horizonal(alien, walls,granularity)
    elif alien.get_shape() == "Vertical":
        return wall_intercept_vertical(alien, walls,granularity)


    return False
#def does_alien_touch_wall(alien, walls,granularity):
    return False
def does_alien_touch_goal(alien, goals):
    """Determine whether the alien touches a goal
        
        Args:
            alien (Alien): Instance of Alien class that will be navigating our map
            goals (list): x, y coordinate and radius of goals in the format [(x, y, r), ...]. There can be multiple goals
        
        Return:
            True if a goal is touched, False if not.
    """
    center_alien = alien.get_centroid()
    #print(center_alien)
    def touch_goal_circle(alien, goals):
        center_alien = alien.get_centroid()
        #print(center_alien)
        r_alien= alien.get_width()
        #print("goals is ",goals)
        for goal in goals:
            #print(goal)
            #print(center_alien)
            dist = np.sqrt((center_alien[0]-goal[0])**2+(center_alien[1]-goal[1])**2)
            #print(dist)
            #print(r_alien)
            #print(goal[2])
            #print((dist < r_alien +goal[2]) or np.isclose(dist, r_alien+goal[2]))
            if (dist < r_alien +goal[2]) or np.isclose(dist, r_alien+goal[2]):
                return True
        #print(walls)
        return False
    
    def touch_goal_horizontal(alien, goals):
        #print('now goal horizontal')
        center_alien = alien.get_centroid()
        width = alien.get_width()
        head = alien.get_head_and_tail()[0]
        tail = alien.get_head_and_tail()[1]
        #print(width)
        #print(center_alien)
        #print(head,tail)

        smallhead = min(head[0],tail[0])
        bighead = max(head[0],tail[0])
        
        class Point:
            def __init__(self,x,y):
                self.x = x
                self.y = y

        a = Point(bighead+width,head[1]-width)#bot right
        b = Point(bighead+width,head[1]+width)#top right
        c = Point(smallhead-width,tail[1]-width)# bot left
        d = Point(smallhead-width,tail[1]+width)#top left
        #print(a.x,a.y,b.x,b.y,c.x,c.y,d.x,d.y)
        for goal in goals:
            #print(goal)
            r = goal[2]
            for point in (a,b,c,d):
                if (goal[0]<=a.x) and (goal[0]>=c.x):
                    if (goal[1]<=b.y+r) and (goal[1]>=a.y-r):
                        return True
                elif (goal[1]<=b.y) and (goal[1]>=a.y):
                    if (goal[0]<=a.x+r) and (goal[0]>=c.x-r):
                        return True
                else:
                    ##print(point.x,point.y)
                    dist = np.sqrt((point.x-goal[0])**2+(point.y-goal[1])**2)
                    #print(dist)
                    if (dist < goal[2]) or np.isclose(dist,goal[2]):
                        return True


        return False


    def touch_goal_vertical(alien, goals):
        center_alien = alien.get_centroid()
        width = alien.get_width()
        head = alien.get_head_and_tail()[0]
        tail = alien.get_head_and_tail()[1]
        #print(width)
        #print(center_alien)
        #print(head,tail)

        smallhead = min(head[0],tail[0])
        bighead = max(head[0],tail[0])
        
        class Point:
            def __init__(self,x,y):
                self.x = x
                self.y = y

        a = Point(head[0]-width,head[1]-width)#bot left
        b = Point(head[0]+width,head[1]-width)#bot right
        c = Point(tail[0]-width,tail[1]+width)#top left
        d = Point(tail[0]+width,tail[1]+width)#top right
        #print(a.x,a.y,b.x,b.y,c.x,c.y,d.x,d.y)
        for goal in goals:
            #print(goal)
            r = goal[2]
            for point in (a,b,c,d):
                if (goal[0]<=a.x) and (goal[0]>=b.x):
                    if (goal[1]<=c.y+r) and (goal[1]>=b.y-r):
                        return True
                elif (goal[1]<=c.y) and (goal[1]>=b.y):
                    if (goal[0]<=b.x+r) and (goal[0]>=c.x-r):
                        return True
                else:
                    ##print(point.x,point.y)
                    dist = np.sqrt((point.x-goal[0])**2+(point.y-goal[1])**2)
                    #print(dist)
                    if (dist < goal[2]) or np.isclose(dist,goal[2]):
                        return True


        return False


    if alien.get_shape() == "Ball":
        return touch_goal_circle(alien, goals)
    elif alien.get_shape() == "Horizontal":
        return touch_goal_horizontal(alien, goals)
    elif alien.get_shape() == "Vertical":
        return touch_goal_vertical(alien, goals)

    return False
#def does_alien_touch_goal(alien, goals):
    """Determine whether the alien touches a goal
        
        Args:
            alien (Alien): Instance of Alien class that will be navigating our map
            goals (list): x, y coordinate and radius of goals in the format [(x, y, r), ...]. There can be multiple goals
        
        Return:
            True if a goal is touched, False if not.
    """
    return False

def is_alien_within_window(alien, window,granularity):
    """Determine whether the alien stays within the window
        
        Args:
            alien (Alien): Alien instance
            window (tuple): (width, height) of the window
            granularity (int): The granularity of the map
    """

    window_lines = [(0,0,0,window[1]),
                    (0,window[1],window[0],window[1]),
                    (window[0],window[1],window[0],0),
                    (window[0],0,0,0)]
    #print(alien.get_head_and_tail())
    #print(alien.get_shape())
    walls = window_lines
    def wall_intercept_circle_window(alien, window,granularity):
        center = alien.get_centroid()
        r = alien.get_width()
        #print(r)
        #print(center)
        #print(walls)
    
        
        for wall in walls:
        #print(wall)
            #print('current wall is ',wall)
            if (wall[2]-wall[0]) != 0: #not vertical line
                slope = (wall[3]-wall[1])/(wall[2]-wall[0])
                #print(slope)
                intercept = wall[1]-slope*wall[0]
                #print(intercept)
                dist_center_to_line = abs(slope*center[0]-center[1]+intercept)/np.sqrt(slope**2+1)
                #print(dist_center_to_line)
                if (dist_center_to_line < r+granularity/np.sqrt(2)) or np.isclose(dist_center_to_line , r+granularity/np.sqrt(2)):
                    min_dist_x_pos = (-1*(-1*center[0]-slope*center[1])-slope*intercept)/(slope*2+1)
                    if (min_dist_x_pos <= max(wall[2], wall[0])) & (min_dist_x_pos >= min(wall[2], wall[0])):
                        return False
                    
            else:  # vertical line   
                #print("shit, vertical line",wall) 
                dist_center_to_line = abs(center[0])
                if dist_center_to_line < (r+granularity/np.sqrt(2)):
                    min_dist_y_pos = center[1]
                    #print('mindist y pos is',min_dist_y_pos)
                    if (min_dist_y_pos < max(wall[3], wall[1])) & (min_dist_y_pos > min(wall[3], wall[1])):
                        return False
                else:
                    #print('min_dist y pos is not in line')
                    continue
                    
        return True
    
    def wall_intercept_horizonal_window(alien, window,granularity):
        #print("now in horizontal")
        #print(window)
        #print(walls)
        center = alien.get_centroid()
        width = alien.get_width()
        head = alien.get_head_and_tail()[0]
        tail = alien.get_head_and_tail()[1]
        #print(width)
        #print(center)
        #print(head,tail)

        smallhead = min(head[0],tail[0])
        bighead = max(head[0],tail[0])


        class Point:
            def __init__(self,x,y):
                self.x = x
                self.y = y

        def ccw(A,B,C):
            return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)

        def intersect(A,B,C,D):
            return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)   


        a = Point(bighead+width,head[1]-width)#bot right
        b = Point(bighead+width,head[1]+width)#top right
        c = Point(smallhead-width,tail[1]-width)# bot left
        d = Point(smallhead-width,tail[1]+width)#top left
        #print(a.x,a.y,b.x,b.y,c.x,c.y,d.x,d.y)
        for wall in walls:
            #print(wall)
            wallPoint_1 = Point(wall[0],wall[1])
            wallPoint_2 = Point(wall[2],wall[3])
            ##print(intersect(a,b,wallPoint_1,wallPoint_2))
            ##print(intersect(b,c,wallPoint_1,wallPoint_2))
            ##print(intersect(c,d,wallPoint_1,wallPoint_2))
            ##print(intersect(d,a,wallPoint_1,wallPoint_2))      
            #print(wallPoint_1.x,wallPoint_1.y,wallPoint_2.x, wallPoint_2.y)  
           # #print(np.isclose(c.x,0) , np.isclose(c.y,0) , np.isclose(b.x,window[0]) , np.isclose(b.y,window[1]))   
            #print(intersect(a,b,wallPoint_1,wallPoint_2) , intersect(a,c,wallPoint_1,wallPoint_2) , intersect(c,d,wallPoint_1,wallPoint_2) ,intersect(d,b,wallPoint_1,wallPoint_2))
            
            if intersect(a,b,wallPoint_1,wallPoint_2) or  intersect(b,c,wallPoint_1,wallPoint_2) or  intersect(c,d,wallPoint_1,wallPoint_2) or intersect(d,a,wallPoint_1,wallPoint_2):
                return False
            elif np.isclose(c.x,0) or np.isclose(c.y,0) or np.isclose(b.x,window[0]) or np.isclose(b.y,window[1]):
                ##print(np.isclose(c.x,0))
               
                #print("wtf")
                return False
        return True

    def wall_intercept_vertical_window(alien, window,granularity):
        #print("now in vertical")
        #print(window)
        #print(walls)
        center = alien.get_centroid()
        width = alien.get_width()
        head = alien.get_head_and_tail()[0]
        tail = alien.get_head_and_tail()[1]
        #print(width)
        #print(center)
        #print(head,tail)

        class Point:
            def __init__(self,x,y):
                self.x = x
                self.y = y

        def ccw(A,B,C):
            return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)

        def intersect(A,B,C,D):
            return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)        
    
        a = Point(head[0]-width,head[1]-width)#bot left
        b = Point(head[0]+width,head[1]-width)#bot right
        c = Point(tail[0]-width,tail[1]+width)# top left
        d = Point(tail[0]+width,tail[1]+width)#top right
        #print(a.x,a.y,b.x,b.y,c.x,c.y,d.x,d.y)
        for wall in walls:
        ##print(wall)
            wallPoint_1 = Point(wall[0],wall[1])
            wallPoint_2 = Point(wall[2],wall[3])
            ##print(intersect(a,b,wallPoint_1,wallPoint_2))
            ##print(intersect(b,c,wallPoint_1,wallPoint_2))
            ##print(intersect(c,d,wallPoint_1,wallPoint_2))
            ##print(intersect(d,a,wallPoint_1,wallPoint_2))   
            #print(wallPoint_1.x,wallPoint_1.y,wallPoint_2.x, wallPoint_2.y)  
         
            #print(intersect(a,b,wallPoint_1,wallPoint_2) , intersect(b,c,wallPoint_1,wallPoint_2) , intersect(c,d,wallPoint_1,wallPoint_2) ,intersect(d,a,wallPoint_1,wallPoint_2))

            if intersect(a,b,wallPoint_1,wallPoint_2) or  intersect(b,c,wallPoint_1,wallPoint_2) or  intersect(c,d,wallPoint_1,wallPoint_2) or intersect(d,a,wallPoint_1,wallPoint_2):
                return False
            elif np.isclose(a.x,0) or np.isclose(a.y,0) or np.isclose(d.x,window[0]) or np.isclose(d.y,window[1]):
                ##print(np.isclose(c.x,0))
               
                #print("wtfvertical")
                return False
                
        return True

    if alien.get_shape() == "Ball":
        return wall_intercept_circle_window(alien, window,granularity)
    elif alien.get_shape() == "Horizontal":
        return wall_intercept_horizonal_window(alien, window,granularity)
    elif alien.get_shape() == "Vertical":
        return wall_intercept_vertical_window(alien, window,granularity)

    #return False



#def is_alien_within_window(alien, window,granularity):
    return True 



if __name__ == '__main__':
    #Walls, goals, and aliens taken from Test1 map
    walls =   [(0,100,100,100),  
                (0,140,100,140),
                (100,100,140,110),
                (100,140,140,130),
                (140,110,175,70),
                (140,130,200,130),
                (200,130,200,10),
                (200,10,140,10),
                (175,70,140,70),
                (140,70,130,55),
                (140,10,130,25),
                (130,55,90,55),
                (130,25,90,25),
                (90,55,90,25)]
    goals = [(110, 40, 10)]
    window = (220, 200)

    #Initialize Aliens and perform simple sanity check. 
    alien_ball = Alien((30,120), [40, 0, 40], [11, 25, 11], ('Horizontal','Ball','Vertical'), 'Ball', window)	
    assert not does_alien_touch_wall(alien_ball, walls, 0), f'does_alien_touch_wall(alien, walls) with alien config {alien_ball.get_config()} returns True, expected: False'
    assert not does_alien_touch_goal(alien_ball, goals), f'does_alien_touch_goal(alien, walls) with alien config {alien_ball.get_config()} returns True, expected: False'
    assert is_alien_within_window(alien_ball, window, 0), f'is_alien_within_window(alien, walls) with alien config {alien_ball.get_config()} returns False, expected: True'

    alien_horz = Alien((30,120), [40, 0, 40], [11, 25, 11], ('Horizontal','Ball','Vertical'), 'Horizontal', window)	
    assert not does_alien_touch_wall(alien_horz, walls, 0), f'does_alien_touch_wall(alien, walls) with alien config {alien_horz.get_config()} returns True, expected: False'
    assert not does_alien_touch_goal(alien_horz, goals), f'does_alien_touch_goal(alien, walls) with alien config {alien_horz.get_config()} returns True, expected: False'
    assert is_alien_within_window(alien_horz, window, 0), f'is_alien_within_window(alien, walls) with alien config {alien_horz.get_config()} returns False, expected: True'

    alien_vert = Alien((30,120), [40, 0, 40], [11, 25, 11], ('Horizontal','Ball','Vertical'), 'Vertical', window)	
    assert does_alien_touch_wall(alien_vert, walls, 0),f'does_alien_touch_wall(alien, walls) with alien config {alien_vert.get_config()} returns False, expected: True'
    assert not does_alien_touch_goal(alien_vert, goals), f'does_alien_touch_goal(alien, walls) with alien config {alien_vert.get_config()} returns True, expected: False'
    assert is_alien_within_window(alien_vert, window, 0), f'is_alien_within_window(alien, walls) with alien config {alien_vert.get_config()} returns False, expected: True'

    edge_horz_alien = Alien((50, 100), [100, 0, 100], [11, 25, 11], ('Horizontal','Ball','Vertical'), 'Horizontal', window)
    edge_vert_alien = Alien((200, 70), [120, 0, 120], [11, 25, 11], ('Horizontal','Ball','Vertical'), 'Vertical', window)

    def test_helper(alien : Alien, position, truths):
        alien.set_alien_pos(position)
        config = alien.get_config()
        assert does_alien_touch_wall(alien, walls, 0) == truths[0], f'does_alien_touch_wall(alien, walls) with alien config {config} returns {not truths[0]}, expected: {truths[0]}'
        assert does_alien_touch_goal(alien, goals) == truths[1], f'does_alien_touch_goal(alien, goals) with alien config {config} returns {not truths[1]}, expected: {truths[1]}'
        assert is_alien_within_window(alien, window, 0) == truths[2], f'is_alien_within_window(alien, window) with alien config {config} returns {not truths[2]}, expected: {truths[2]}'

    alien_positions = [
                        #Sanity Check
                        (0, 100),

                        #Testing window boundary checks
                        (25.6, 25.6),
                        (25.5, 25.5),
                        (194.4, 174.4),
                        (194.5, 174.5),

                        #Testing wall collisions
                        (30, 112),
                        (30, 113),
                        (30, 105.5),
                        (30, 105.6), # Very close edge case
                        (30, 135),
                        (140, 120),
                        (187.5, 70), # Another very close corner case, right on corner
                        
                        #Testing goal collisions
                        (110, 40),
                        (145.5, 40), # Horizontal tangent to goal
                        (110, 62.5), # ball tangent to goal
                        
                        #Test parallel line oblong line segment and wall
                        (50, 100),
                        (200, 100),
                        (205.5, 100) #Out of bounds
                    ]

    #Truths are a list of tuples that we will compare to function calls in the form (does_alien_touch_wall, does_alien_touch_goal, is_alien_within_window)
    alien_ball_truths = [
                            (True, False, False),
                            (False, False, True),
                            (False, False, True),
                            (False, False, True),
                            (False, False, True),
                            (True, False, True),
                            (False, False, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True),
                            (False, True, True),
                            (False, False, True),
                            (True, True, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True)
                        ]
    alien_horz_truths = [
                            (True, False, False),
                            (False, False, True),
                            (False, False, False),
                            (False, False, True),
                            (False, False, False),
                            (False, False, True),
                            (False, False, True),
                            (True, False, True),
                            (False, False, True),
                            (True, False, True),
                            (False, False, True),
                            (True, False, True),
                            (True, True, True),
                            (False, True, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, False),
                            (True, False, False)
                        ]
    alien_vert_truths = [
                            (True, False, False),
                            (False, False, True),
                            (False, False, False),
                            (False, False, True),
                            (False, False, False),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True),
                            (False, False, True),
                            (True, True, True),
                            (False, False, True),
                            (True, True, True),
                            (True, False, True),
                            (True, False, True),
                            (True, False, True)
                        ]

    for i in range(len(alien_positions)):
        test_helper(alien_ball, alien_positions[i], alien_ball_truths[i])
        test_helper(alien_horz, alien_positions[i], alien_horz_truths[i])
        test_helper(alien_vert, alien_positions[i], alien_vert_truths[i])

    #Edge case coincide line endpoints
    test_helper(edge_horz_alien, edge_horz_alien.get_centroid(), (True, False, False))
    test_helper(edge_horz_alien, (110,55), (True, True, True))
    test_helper(edge_vert_alien, edge_vert_alien.get_centroid(), (True, False, True))


    print("Geometry tests passed\n")