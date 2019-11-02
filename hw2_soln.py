'''
CS461 Homework 2

Nickname of the Group: RUNTIME TERROR

Group Members:
Emre Tolga Ayan
Munib Emre Sevilgen
Kürşad Kaan Atilla
Muhammed Berk Köse
Arkun Bozkurt

Part A:
We have used a heuristic function for a A* search algorithm. 
This heuristic function adds the number of cannibals and the 
missionaries at the west side of the river. By this approach
we can understand how close the algorithm is to the desired 
state. We add this heuristic function with the length of the
existing path to sort the queue during A* search.

Part B:
We have use depth first search to reach the desired state. 
We compare the length of the new path with the shortest path 
we have found before. When we find a shorter path, we delete
all the existing paths.
'''

import re
from node import Node

# =============================================================================================================================================

def check_input_validity(state):  
    # Regular Expression statement is used to check the input format      
    state_exp  = re.search("\dM\dC\d", state)     
    if state_exp is None:
        print("Error in input. Syntax should be in the following format: xMyCb")
        return False
    else:
        # Check whether the b is valid or not
        b = int(state[4]) 
        if b == 0 or b == 1:
            return True
        return False

def get_legal_states(node, m, c, bc):
    legal_states = []

    # Get the last state data at the path
    current_data = node._path[len(node._path)-1]
    m_w = current_data[0]
    c_w = current_data[1]
    m_e = m - m_w
    c_e = c - c_w

    # Get all the numbers of people we can carry with the boat
    for no_of_person in range(1,bc+1):
        # Get all the numbers of cannibals to carry
        for c_no_of_person in range(no_of_person+1):
            # Calculate the numbers of missionaries to carry
            m_no_of_person = no_of_person-c_no_of_person
            # Compare the number of people in the boat
            if m_no_of_person>=c_no_of_person or m_no_of_person == 0 or c_no_of_person == 0:
                # For west side
                if current_data[2] == 1:
                    # Check whether there are enough person at the land
                    if m_no_of_person <= m_w and c_no_of_person <= c_w:
                        m_new_w = m_w - m_no_of_person
                        c_new_w = c_w - c_no_of_person
                        m_new_e = m_e + m_no_of_person
                        c_new_e = c_e + c_no_of_person
                        
                        # Compare the number of people in the lands
                        if (m_new_w >= c_new_w or m_new_w == 0 or c_new_w == 0) and (m_new_e >= c_new_e or m_new_e == 0 or c_new_e == 0):
                            legal_states.append([m_new_w,c_new_w,0])
                
                # For east side
                else:
                    # Check whether there are enough person at the land
                    if m_no_of_person <= m_e and c_no_of_person <= c_e:
                        m_new_w = m_w + m_no_of_person
                        c_new_w = c_w + c_no_of_person
                        m_new_e = m_e - m_no_of_person
                        c_new_e = c_e - c_no_of_person
                        
                        # Compare the number of people in the lands
                        if (m_new_w >= c_new_w or m_new_w == 0 or c_new_w == 0) and (m_new_e >= c_new_e or m_new_e == 0 or c_new_e == 0):
                            legal_states.append([m_new_w,c_new_w,1])

    return legal_states

  

def get_new_nodes(node, legal_states):
    new_nodes = []
    for state in legal_states:
        # To ignore the circles, search the existing path
        circle = True
        for ex_state in node._path:
            if (ex_state == state):
                circle = False
        # If the state is new
        if (circle):
            new_node = Node()
            # Add the existing states at the path
            for ex_state in node._path:
                new_node.add_to_path(ex_state)
            # Add the new state to the path
            new_node.add_to_path(state)
            new_nodes.append(new_node)

    return new_nodes

def print_progress_info(node):    
    print("Current node path    : ", end = " ")
    for state in node.get_path():
        print("'"+str(state[0])+"M"+str(state[1])+"C"+str(state[2]), end="' ")
    print()

def print_sequence(node): 
    print("\nThe output:")
    # Print initial state
    cur_state = node._path[0]
    for i in range(cur_state[0]):
        print('C', end='')
     
    print()

    for i in range(cur_state[1]):
        print('M', end='')
    print()

    m = cur_state[0]
    c = cur_state[1]

    # Print other states
    for i in range(1,len(node._path)):
        prev_state = node._path[i-1]
        cur_state = node._path[i]
        c_prev = prev_state[1]
        c_cur = cur_state[1]
        m_prev = prev_state[0]
        m_cur = cur_state[0]
        
        print()
        # Print the SEND or RETURN
        if (cur_state[2]==0):
            print("SEND",end="\t")
        else:
            print("RETURN",end="\t")
        
        # Print the number of cannibals and missionaries to carry
        print(str(abs(c_cur-c_prev)) + " CANNIBALS " + str(abs(m_cur-m_prev)) + " MISSIONARIES")

        # Print the cannibals at west side
        for i in range(cur_state[1]):
            print('C',end='')
        print("\t\t"+"      ",end='')
        
        # Print the cannibals at east side
        for i in range(c-cur_state[1]):
            print('C',end='')

        print()

        # Print the missionaries at west side
        for i in range(cur_state[0]):
            print('M',end='')
        print("\t\t"+"      ",end='')

        # Print the missionaries at west side
        for i in range(c-cur_state[0]):
            print('M',end='')
        print()
        cur_state = node._path[0]


def a_star_search(init_state, result_state, boat_cap):
    # Create the initial root node and add initial state to its path
    rootNode = Node()
    rootNode.add_to_path(init_state)

    # Initial M and C values
    m = init_state[0]
    c = init_state[1]

    # Create a new queue with the initial root node
    s = []
    s.append(rootNode)

    # This will hold the solution if it exists
    soln_path = []

    while not len(s) == 0:  
        current_node  = s.pop(0)
        legal_states  = get_legal_states(current_node, m, c, boat_cap)

        # Print progress info
        print_progress_info(current_node)

        # Check if solution found or not. If found, break the loop and return the path
        if  result_state in legal_states:
            current_node.add_to_path(result_state)
            print_progress_info(current_node)
            print_sequence(current_node)
            return current_node.get_path()
        
        # Get new nodes with new legal states
        new_nodes = get_new_nodes(current_node, legal_states)
        
        # Eliminate the paths that reachs the same node. Only the path has minimum cost is left.
        for new_node in new_nodes:
            check = False
            for node in s:
                path_1 = new_node._path
                path_2 = node._path
                cur_state_1 = path_1[-1]
                cur_state_2 = path_2[-1]

                # Check the states are same or not
                if cur_state_1 == cur_state_2:
                    check = True
                    # Remove the longer path if there is a shorter one
                    if len(path_1) < len (path_2):
                        s.remove(node)
                        s.append(new_node)
                    break
            # If there is not any other path to the state, add it to the queue
            if not check:
                s.append(new_node)

        # Sort the paths by the sum of the heuristics and the cost of the path by the node class
        s.sort()
    return None

def dfs_search_all_sequences(init_state, result_state, boat_cap):
    # Create the initial root node and add initial state to its path
    rootNode = Node()
    rootNode.add_to_path(init_state)

    # Initial M and C values
    m = init_state[0]
    c = init_state[1]

    # Create a new queue with the initial root node
    s = []
    s.append(rootNode)

    # This will hold the sequences if exists
    sequences = []
    shortestPathLength = -1

    while not len(s) == 0:  
        current_node  = s.pop()
        legal_states  = get_legal_states(current_node, m, c, boat_cap)

        # Print progress info
        print_progress_info(current_node)

        # Check if solution found or not. If found add it to the sequences
        if  result_state in legal_states:
            current_node.add_to_path(result_state)
            print_progress_info(current_node)
            soln_path = []
            for state in current_node.get_path():
                soln_path.append(str(state[0])+"M"+str(state[1])+"C"+str(state[2]))
            
            length = len(soln_path)
            newSequences = []
            # If the length of the new path is equal to the shortest path so far or the path is the first add it to the sequences
            if length == shortestPathLength or shortestPathLength == -1:
                sequences.append(soln_path)
                shortestPathLength = length

            # If the length of the new path is smaller than the shortest path, delete all the sequences and update the shortest path
            elif length < shortestPathLength:
                shortestPathLength = length
                newSequences.append(soln_path)
                sequences = newSequences
        
        # Get new nodes with new legal states
        new_nodes = get_new_nodes(current_node, legal_states)       
        for new_node in new_nodes:
            s.append(new_node)
        
        # Check the path lengths to get rid of the longer paths
        sNew = []
        for node in s:
            if len(node._path) <= shortestPathLength or shortestPathLength == -1:
                sNew.append(node)
        s = sNew

    return sequences
    
# =============================================================================================================================================


# Part A
print("Part A\n------\n")

# Get and check initial state input data
while True:
    # init_state_data = str(input("Enter initial state:"))
    init_state_data = "6M6C1"

    if check_input_validity(init_state_data) is True:
        break
    
# Get and check result state input data
while True:
    # result_state_data = str(input("Enter desired state:"))
    result_state_data = "0M0C0"

    if check_input_validity(result_state_data) is True:
        break

# Get and check boat capacity input data
while True:
    # boat_capacity = int(input("Enter the boat capacity:"))
    boat_capacity = 5

    if boat_capacity > 0:
        break

init_state = [int(init_state_data[0]),int(init_state_data[2]),int(init_state_data[4])]
result_state = [int(result_state_data[0]),int(result_state_data[2]),int(result_state_data[4])]

print("A* Search:")
soln_path = a_star_search(init_state, result_state, boat_capacity)        

# Print info message
if len(soln_path) == None:
    print("No solutions found.")

# Part B
print("\nPart B\n------")
init_state = [4,4,1]
result_state = [0,0,0]
boat_capacity = 3

print("DFS:")
sequences = dfs_search_all_sequences(init_state, result_state, boat_capacity)    

# Print the number of shortest sequences and the sequnces themselves
print("\nThe number of shortest sequences:",len(sequences))
print("\nThe sequences:")
for i in range(len(sequences)):
    print(i+1, '-', sequences[i])
    

wait = input("\n\nPress enter to exit")



        