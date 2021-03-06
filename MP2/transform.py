
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
import re

from numpy import ndindex
# from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *



def transformToMaze(alien, goals, walls, window,granularity):
    """This function transforms the given 2D map to the maze in MP1.
    
        Args:
            alien (Alien): alien instance
            goals (list): [(x, y, r)] of goals
            walls (list): [(startx, starty, endx, endy)] of walls
            window (tuple): (width, height) of the window
 
        Return:
            Maze: the maze instance generated based on input arguments. 

    """
    #center = alien.get_centroid()
    #print(alien.get_width())
    initial_config = tuple(alien.get_config())
    #print(initial_config)
    #shapeid = alien.get_shape_idx()
    #print(center)
    rows = int(window[0]/granularity +1)
    cols = int(window[1]/granularity +1)
    #startingrow = int(center[0]/granularity) +1
    #startingcol = int(center[1]/granularity) +1
    maze = np.full((rows,cols,3),SPACE_CHAR)
    #print(len(maze),len(maze[0]),len(maze[0][0]))

    
    #alien.set_alien_shape("Ball")
    #level = alien.get_shape_idx()
    #print(level)
    for idxs in np.ndindex((rows,cols,3)):
        #print(idxs)
        #if alien.get_shape() == "Horizontal":
            #print(alien.get_width())
            #print(alien.get_head_and_tail())
        flag = False
        config  = idxToConfig(idxs, [0,0,0], granularity,alien)
        #print(config)
        alien.set_alien_config(config)
       # if config[0] == center[0] and config[1] == center[1] and config[2] == shapeid:
        if config == initial_config:
            maze[idxs] = START_CHAR
            flag = True
        elif does_alien_touch_wall(alien, walls, granularity):
            maze[idxs] = WALL_CHAR
        elif not is_alien_within_window(alien, window, granularity):
            maze[idxs] = WALL_CHAR      
        elif does_alien_touch_goal(alien,goals):
            maze[idxs] = OBJECTIVE_CHAR      
            
    if flag == False:
        maze[initial_config[0]//granularity][initial_config[1]//granularity][1] = START_CHAR
    
    mazelist= maze.tolist()
    finalmaze = Maze(mazelist,alien)
    print("done2")
    return finalmaze

    pass

    

if __name__ == '__main__':
    import configparser


    def generate_test_mazes(granularities,map_names):
        for granularity in granularities:
            for map_name in map_names:
                configfile = './maps/test_config.txt'
                config = configparser.ConfigParser()
                config.read(configfile)
                lims = eval(config.get(map_name, 'Window'))
                # print(lis)
                # Parse config file
                window = eval(config.get(map_name, 'Window'))
                centroid = eval(config.get(map_name, 'StartPoint'))
                widths = eval(config.get(map_name, 'Widths'))
                alien_shape = 'Ball'
                lengths = eval(config.get(map_name, 'Lengths'))
                alien_shapes = ['Horizontal','Ball','Vertical']
                obstacles = eval(config.get(map_name, 'Obstacles'))
                boundary = [(0,0,0,lims[1]),(0,0,lims[0],0),(lims[0],0,lims[0],lims[1]),(0,lims[1],lims[0],lims[1])]
                obstacles.extend(boundary)
                goals = eval(config.get(map_name, 'Goals'))
                alien = Alien(centroid,lengths,widths,alien_shapes,alien_shape,window)
                print('transforming map to maze')
                generated_maze = transformToMaze(alien,goals,obstacles,window,granularity)
                generated_maze.saveToFile('./mazes/{}_granularity_{}.txt'.format(map_name,granularity))
    
    def compare_test_mazes_with_gt(granularities,map_names):
        name_dict = {'%':'walls','.':'goals',' ':'free space','P':'start'}
        shape_dict = ['Horizontal','Ball','Vertical']
        for granularity in granularities:
            for map_name in map_names:
                if(map_name == 'NoSolutionMap' and granularity == 10):
                    continue
                this_maze_file = './mazes/{}_granularity_{}.txt'.format(map_name,granularity)
                gt_maze_file = './mazes/gt_{}_granularity_{}.txt'.format(map_name,granularity)
                gt_maze = Maze([],[],[],filepath = gt_maze_file)
                this_maze = Maze([],[],[],filepath= this_maze_file)
                gt_map = np.array(gt_maze.get_map())
                this_map = np.array(this_maze.get_map())
                assert gt_map.shape == this_map.shape, "Mazes have different Shapes! Did you use idxToConfig and ConfigToIdx when generating your map?"
                difx,dify,difz = np.where(gt_map != this_map)
                if(difx.size != 0):
                    diff_dict = {}
                    for i in ['%','.',' ','P']:
                        for j in ['%','.',' ','P']:
                            diff_dict[i + '_'+ j] = []
                    print('\n\nDifferences in {} at granularity {}:'.format(map_name,granularity))    
                    for i,j,k in zip(difx,dify,difz):
                        gt_token = gt_map[i][j][k] 
                        this_token = this_map[i][j][k]
                        diff_dict[gt_token + '_' + this_token].append(noAlienidxToConfig((i,j,k),granularity,shape_dict))
                    for key in diff_dict.keys():
                        this_list = diff_dict[key]
                        gt_token = key.split('_')[0]
                        your_token = key.split('_')[1]
                        if(len(this_list) != 0):
                            print('Ground Truth {} mistakenly identified as {}: {}\n'.format(name_dict[gt_token],name_dict[your_token],this_list))
                        
                    print('\n\n')

    granularities = [8]
    map_names = ['Test1']
    generate_test_mazes(granularities,map_names)
    compare_test_mazes_with_gt(granularities,map_names)