
# coding: utf-8

# In[129]:


# Antonius Panggabean (861232158)
# CS170 Project 1: 8-Puzzle  

import queue as q
from copy import deepcopy

# goal state and preset puzzles
goal_state = [[1,2,3],
              [4,5,6],
              [7,8,0]]

very_easy = [[1,2,3],
             [4,5,6],
             [7,0,8]]

easy = [[1,2,0],
        [4,5,3],
        [7,8,6]]

doable = [[0,1,2],
          [4,5,3],
          [7,8,6]]

oh_boy = [[8,7,1],
          [6,0,2],
          [5,4,3]]

impossible = [[1,2,3],
              [4,5,6],
              [8,7,0]]

################## Program Functions ################## 

def show_puzzle(puzzle):
    for i in range(0,3):
        print(puzzle[i][0],puzzle[i][1],puzzle[i][2])
    return


def num_misplaced_tiles(puzzle):
    count = 0
    k = 1
    for i in range(0,3):
        for j in range(0,3):
            if puzzle[i][j] != k:
                count += 1;
            k+=1
    return count-1 


def find_position(puzzle, num):
    for i in range(0,3):
        for j in range(0,3):
            if puzzle[i][j] == num:
                return [i, j]
    return [-1, -1]


def manhattan_distance(puzzle):
    count = 0;
    k = 1
    for i in range(0,3):
        for j in range(0,3):
            if puzzle[i][j] != 0:
                if puzzle[i][j] != k:
                    num_pos = find_position(puzzle,k)
                    count = count + abs(num_pos[0]-i) + abs(num_pos[1]-j)
            k+=1    
    return count


def uniform(nodes, expanded_nodes):
    for i in expanded_nodes:
        nodes.put([i.depth,i])
    return

def A_star_misplaced_tiles(nodes, expanded_nodes):
    for i in expanded_nodes:
        nodes.put([i.depth+num_misplaced_tiles(i.state),i])
    return

def A_star_manhattan(nodes, expanded_nodes):
    for i in expanded_nodes:
        nodes.put([i.depth+manhattan_distance(i.state),i])
    return


# simple node class with depth values
class Node:
    def __init__(self, state, depth):
        self.state = state
        self.depth = depth
        return
    
    def __lt__(self, other):
        return self.depth < other.depth


# problem class according to general search algorithm
class Problem:
    
    # initialize problem class 
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.history = list()
        return
    
    # simply uses a heuristic function which returns 0 if goal state reached 
    def goal_test(self, node_state):
        return num_misplaced_tiles(node_state) == 0
    
    # checks if each operator is valid and create new nodes to add to queue
    def operators(self, current_state, current_depth):
        
        [by, bx] = find_position(current_state, 0)
        expanded_nodes = []
        
        # left
        if bx > 0:
            # append left move
            Lmat = deepcopy(current_state)
            Lmat[by][bx-1], Lmat[by][bx] = Lmat[by][bx], Lmat[by][bx-1]
            Lnode = Node(Lmat, current_depth+1)
            if Lnode.state not in self.history:
                self.history.append(Lnode.state)
                expanded_nodes.append(Lnode)
                
        # right
        if bx < 2:
            # append right move
            Rmat = deepcopy(current_state)
            Rmat[by][bx+1], Rmat[by][bx] = Rmat[by][bx], Rmat[by][bx+1]
            Rnode = Node(Rmat, current_depth+1)
            if Rnode.state not in self.history:
                self.history.append(Rnode.state)
                expanded_nodes.append(Rnode)
                
        # up
        if by > 0:
            # append up move
            Umat = deepcopy(current_state)
            Umat[by-1][bx], Umat[by][bx] = Umat[by][bx], Umat[by-1][bx]
            Unode = Node(Umat, current_depth+1)
            if Unode.state not in self.history:
                self.history.append(Unode.state)
                expanded_nodes.append(Unode)
                
        # down
        if by < 2:
            # append down move
            Dmat = deepcopy(current_state)
            Dmat[by+1][bx], Dmat[by][bx] = Dmat[by][bx], Dmat[by+1][bx]
            Dnode = Node(Dmat, current_depth+1)
            if Dnode.state not in self.history:
                self.history.append(Dnode.state)
                expanded_nodes.append(Dnode)
                
        return expanded_nodes


# GENERAL SEARCH FUNCTION FOR ALL ALGORITHMS
def general_search(problem, queueing_function):
    global total_searched
    global max_queue_size
    
    nodes = q.PriorityQueue()
    node = Node(problem.initial_state, 0)
    nodes.put([1, node])
    
    while(1):
        if nodes.empty(): return "failure"
        
        max_queue_size = max(nodes.qsize(),max_queue_size)
        best_node = nodes.get()
        priority = best_node[0]
        node = best_node[1]
        
        if problem.goal_test(node.state): return node
        
        print("The best state to expand with a g(n) =", node.depth,               "and h(n) =", priority-node.depth, "is...")
        show_puzzle(node.state)
        print("   Expanding this node...\n")
        total_searched+=1
        queueing_function(nodes, problem.operators(node.state, node.depth))
    return



###################### START 8-PUZZLE SOLVER PROGRAM ######################

## Choose puzzle selection
p_select = input("Welcome to Antonius Panggabeans 8-puzzle solver.\n"                  "Type \"1\" to use a default puzzle, or \"2\" to enter your own puzzle.\n")

    # Choose default puzzle
if p_select == '1':
    print("default puzzle selected")
    full_puzzle = oh_boy
    
    # Choose create own puzzle
if p_select == '2':
    print("\t Enter your puzzle, use a zero to represent the blank")
    p_row1 = input("\t Enter the first row, use space or tabs between numbers   ").split()
    p_row2 = input("\t Enter the second row, use space or tabs between numbers  ").split()
    p_row3 = input("\t Enter the third row, use space or tabs between numbers   ").split()

    for i in range(0,3):
        p_row1[i] = int(p_row1[i])
        p_row2[i] = int(p_row2[i])
        p_row3[i] = int(p_row3[i])
    full_puzzle = [ p_row1, p_row2, p_row3 ]

problem = Problem(full_puzzle)


## Choose search algorithm and run solver
alg_select = input("\n\t Enter your choice of algorithm\n"                    "\t\t 1. Uniform Cost Search\n"                    "\t\t 2. A* with the Misplaced Tile heuristic.\n"                    "\t\t 3. A* with the Manhattan distance heuristic.\n\n\t\t ")

total_searched = 0
max_queue_size = 0
solution = Node("", 0)

if alg_select == "1":
    heuristic = uniform
if alg_select == "2": 
    heuristic = A_star_misplaced_tiles
if alg_select == "3": 
    heuristic = A_star_manhattan

solution = general_search(problem, heuristic)

## Show results
print("\n\nGoal!!\n")
print("To solve this problem the search algorithm expanded a total of", total_searched, "nodes."      "\nThe maximum number of nodes in the queue at any one time was", max_queue_size, "nodes."      "\nThe depth of the goal node was", solution.depth)

