#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.

'''
rushhour STATESPACE
'''
#   You may add only standard python imports---i.e., ones that are automatically
#   available on CDF.
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

from search import *
from random import randint

##################################################
# The search space class 'rushhour'             #
# This class is a sub-class of 'StateSpace'      #
##################################################


class rushhour(StateSpace):
    def __init__(self, action, gval, parent, vehicle, board_size, goal_entrance, goal_orientation):
#IMPLEMENT
        """Initialize a rushhour search state object."""
        StateSpace.__init__(self, action, gval, parent)
        self.vehicle = vehicle
        self.board_size = board_size
        self.goal_entrance = goal_entrance
        self.goal_orientation = goal_orientation
        
    def successors(self):
#IMPLEMENT
        '''Return list of rushhour objects that are the successors of the current object'''
        origin = self.vehicle
        successors = []
        
        itself = rushhour(self.action, self.gval, self.parent, self.vehicle, self.board_size, self.goal_entrance, self.goal_orientation)
        for v in origin:
            if v[3] == True:
                #west
                copy1 = v[:]
                location1 = copy1[1]                
                copy1[1] = self.move_vehicle(copy1[0], 'W') ##not changed
                mod1 = []
                for c in origin:
                    if c[0] != v[0]:
                        mod1.append(c)
                mod1.append(copy1)
                if copy1[1] != location1:
                    
                    successors.append(rushhour("move_vehicle("+v[0]+", W)", self.gval + 1, itself, mod1, self.board_size, self.goal_entrance, self.goal_orientation))
                #east
                
                copy2 = v[:]
                location2 = copy2[1]
                copy2[1] = self.move_vehicle(copy2[0], 'E') ##not changed
                mod2 = []
                
                for c in origin:
                    if c[0] != v[0]:
                        mod2.append(c)
                mod2.append(copy2)
                if copy2[1] != location2:
                    
                    successors.append(rushhour("move_vehicle("+v[0]+", E)", self.gval + 1, itself, mod2, self.board_size, self.goal_entrance, self.goal_orientation)) 
            if v[3] == False:
                #North
                copy1 = v[:]
                location1 = copy1[1]                
                copy1[1] = self.move_vehicle(copy1[0], 'N') ##not changed
                mod1 = []
                for c in origin:
                    if c[0] != v[0]:
                        mod1.append(c)
                mod1.append(copy1)
                if copy1[1] != location1:
                    
                    successors.append(rushhour("move_vehicle("+v[0]+", N)", self.gval + 1, itself, mod1, self.board_size, self.goal_entrance, self.goal_orientation))
                #south
                
                copy2 = v[:]
                location2 = copy2[1]
                copy2[1] = self.move_vehicle(copy2[0], 'S') ##not changed
                mod2 = []
                
                for c in origin:
                    if c[0] != v[0]:
                        mod2.append(c)
                mod2.append(copy2)
                if copy2[1] != location2:
                    
                    successors.append(rushhour("move_vehicle("+v[0]+", S)", self.gval + 1, itself, mod2, self.board_size, self.goal_entrance, self.goal_orientation)) 
                
               
        return successors      
        ##for x in successors:
            ##self.print_state(x)
        ##print('3')   
    def hashable_state(self):
#IMPLEMENT
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent the state.'''
        key = []
        for vehicle in self.vehicle:
            key.append(tuple(vehicle))
        key.sort()  
        return tuple(key)
    
    def print_state(self):
        #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
        #and in generating sample trace output.
        #Note that if you implement the "get" routines
        #(rushhour.get_vehicle_statuses() and rushhour.get_board_size())
        #properly, this function should work irrespective of how you represent
        #your state.

        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))

        print("Vehicle Statuses")
        for vs in sorted(self.get_vehicle_statuses()):
            print("    {} is at ({}, {})".format(vs[0], vs[1][0], vs[1][1]), end="")
        board = get_board(self.get_vehicle_statuses(), self.get_board_properties())
        print('\n')
        print('\n'.join([''.join(board[i]) for i in range(len(board))]))

#Data accessor routines.

    def get_vehicle_statuses(self):
#IMPLEMENT
        '''Return list containing the status of each vehicle
           This list has to be in the format: [vs_1, vs_2, ..., vs_k]
           with one status list for each vehicle in the state.
           Each vehicle status item vs_i is itself a list in the format:
                 [<name>, <loc>, <length>, <is_horizontal>, <is_goal>]
           Where <name> is the name of the vehicle (a string)
           <loc> is a location (a pair (x,y)) indicating the front of the vehicle,
                       i.e., its length is counted in the positive x- or y-direction
                       from this point
                 <length> is the length of that vehicle
                 <is_horizontal> is true iff the vehicle is oriented horizontally
                 <is_goal> is true iff the vehicle is a goal vehicle
        '''
        return self.vehicle
        
        
    def get_board_properties(self):
#IMPLEMENT
        '''Return (board_size, goal_entrance, goal_direction)
           where board_size = (m, n) is the dimensions of the board (m rows, n columns)
                 goal_entrance = (x, y) is the location of the goal
                 goal_direction is one of 'N', 'E', 'S' or 'W' indicating
                                the orientation of the goal
        '''
        return (self.board_size, self.goal_entrance, self.goal_orientation)
    
    def move_vehicle(self, name, direction):
        (u, w) = self.board_size
        for v in self.vehicle:
            (x, y) = v[1]       
            if v[0] == name:
                if v[3] == False:
                    if direction == 'N':                        
                        if (y - 1) < 0: 
                            if self.not_occupied((x, u - 1)):
                                return (x, u - 1)
                                ##v[1][1] = u - 1
                            else:
                                return (x, y)
                                
                        else:
                            if self.not_occupied((x, y - 1)):
                                return (x, y - 1)
                                ##v[1][1] = y - 1
                            else:
                                return (x, y)
                    elif direction == 'S':
                        if (y + v[2] -1) > (u - 1):                     
                            if self.not_occupied((x, u - y -v[2] + 2)):
                                if y < u - 1:
                                    return (x, y + 1)
                                    ##v[1][1] = y + 1
                                if y == u - 1:
                                    return (x, 0)
                                    ##v[1][1] = 0
                            else:
                                return (x, y)
                        elif (y + v[2] -1) == (u - 1):
                            if self.not_occupied((x, 0)):
                                if y == u - 1:
                                    return (x, 0)
                                    ##v[1][1] = 0
                                else:
                                    return (x, y + 1) 
                                    ##v[1][1] = y + 1
                            else:
                                return (x, y)
                        else:    
                            if self.not_occupied((x, y + v[2])):
                                if y + 1 <= u - 1:                                    
                                    return (x, y + 1)
                                    ##v[1][1] = y + 1
                            else:
                                return (x, y)
                                    
                else:
                    if direction == 'W':                        
                        if (x - 1) < 0:
                            if self.not_occupied((u - 1, y)):
                                return (u - 1, y)
                                ##v[1][0] = u - 1
                            else:
                                return (x, y)
                        else:
                            if self.not_occupied((x - 1, y)):
                                return (x - 1, y)
                                ##v[1][0] = x - 1
                            else:
                                return (x, y)
                    elif direction == 'E':
                        if (x + v[2] -1) > (u - 1):                     
                            if self.not_occupied((u - x -v[2] + 2, y)):
                                if x < u - 1:
                                    return (x + 1, y)
                                    ##v[1][0] = x + 1
                                if x == u - 1:
                                    return (0, y) 
                                    ##v[1][0] = 0
                            else:
                                return (x, y)
                        elif (x + v[2] -1) == (u - 1):
                            if self.not_occupied((0, y)):
                                if x == u - 1:
                                    return (0, y)
                                    ##v[1][0] = 0
                                else:
                                    return (x + 1, y) 
                                    ##v[1][0] = x + 1
                            else:
                                return (x, y)
                        else:    
                            if self.not_occupied((x + v[2], y)):
                                if x + 1 <= u - 1:                                    
                                    return (x + 1, y)
                                    ##v[1][0] = x + 1
                            else:
                                return (x, y)  
                    
    def not_occupied(self, location):
        x = 0
        (c, d) = location
        (u, w) = self.board_size
        for v in self.vehicle:
            if v[3]:
                (a, b) = v[1]              
                if u - a < v[2]:
                    if d == b and a <= c <= u - 1:
                        x += 1
                    elif d == b and 0 <= c <= v[2] - u + a - 1:
                        x += 1
                else:
                    if d == b and a <= c <= (a + v[2] - 1):
                        x += 1
                
            if not v[3]:
                (a, b) = v[1]
                            
                if w - b < v[2]:
                    if a == c and b <= d <= w - 1:
                        x += 1
                    elif a == c and 0 <= d <= v[2] - w + b - 1:
                        x += 1
                else:
                    if a == c and b <= d <= (b + v[2] - 1):
                        x += 1
        if x == 0:
            return True
        else:
            return False
    
                    
                    


        
#############################################
# heuristics                                #
#############################################


def heur_zero(state):
    '''Zero Heuristic use to make A* search perform uniform cost search'''
    return 0


def heur_min_moves(state):
#IMPLEMENT
    '''rushhour heuristic'''
    #We want an admissible heuristic. Getting to the goal requires
    #one move for each tile of distance.
    #Since the board wraps around, there are two different
    #directions that lead to the goal.
    #NOTE that we want an estimate of the number of ADDITIONAL
    #     moves required from our current state
    #1. Proceeding in the first direction, let MOVES1 =
    #   number of moves required to get to the goal if it were unobstructed
    #2. Proceeding in the second direction, let MOVES2 =
    #   number of moves required to get to the goal if it were unobstructed
    #
    #Our heuristic value is the minimum of MOVES1 and MOVES2 over all goal vehicles.
    #You should implement this heuristic function exactly, even if it is
    #tempting to improve it.
    (u, w) = state.board_size
    minh = 10000000
    for v in state.vehicle:
        if v[4]:
            if v[3]:
                (a, b) = v[1]
                (x, y) = state.goal_entrance
                if state.goal_orientation == 'W':
                    if a < x:
                        MOVES1 = x - a
                        MOVES2 = w - x + a
                        if min(MOVES1, MOVES2) <= minh:
                            minh = min(MOVES1, MOVES2)
                    elif a >= x:
                        MOVES1 = a - x
                        MOVES2 = w - a + x
                        if min(MOVES1, MOVES2) <= minh:
                            minh = min(MOVES1, MOVES2)                    
                elif state.goal_orientation == 'E':
                    if (a + v[2] - 1) <= (w - 1):
                        if (a + v[2] - 1) <= x:
                            MOVES1 = x - (a + v[2] - 1)
                            MOVES2 = w - MOVES1
                            if min(MOVES1, MOVES2) <= minh:
                                minh = min(MOVES1, MOVES2)
                        elif (a + v[2] - 1) > x:
                            MOVES1 = (a + v[2] - 1) - x
                            MOVES2 = w - MOVES1
                            if min(MOVES1, MOVES2) <= minh:
                                minh = min(MOVES1, MOVES2)                            
                    elif (a + v[2] - 1) > (w - 1):
                        tail = a + v[2] - 1 - w + 1 - 1
                        if tail <= x:
                            MOVES1 = x - (a + v[2] - 1)
                            MOVES2 = w - MOVES1
                            if min(MOVES1, MOVES2) <= minh:
                                minh = min(MOVES1, MOVES2) 
                        elif tail > x:
                            MOVES1 = (a + v[2] - 1) - x
                            MOVES2 = w - MOVES1
                            if min(MOVES1, MOVES2) <= minh:
                                minh = min(MOVES1, MOVES2)   
                elif state.goal_orientation == 'N':
                    if b < y:
                        MOVES1 = y - b
                        MOVES2 = u - y + b
                        if min(MOVES1, MOVES2) <= minh:
                            minh = min(MOVES1, MOVES2)
                    elif b >= y:
                        MOVES1 = b - y
                        MOVES2 = u - b + y
                        if min(MOVES1, MOVES2) <= minh:
                            minh = min(MOVES1, MOVES2)                    
                elif state.goal_orientation == 'S':
                    if (b + v[2] - 1) <= (u - 1):
                        if (b + v[2] - 1) <= y:
                            MOVES1 = y - (b + v[2] - 1)
                            MOVES2 = u - MOVES1
                            if min(MOVES1, MOVES2) <= minh:
                                minh = min(MOVES1, MOVES2)
                        elif (b + v[2] - 1) > y:
                            MOVES1 = (b + v[2] - 1) - y
                            MOVES2 = u - MOVES1
                            if min(MOVES1, MOVES2) <= minh:
                                minh = min(MOVES1, MOVES2)                          
                    elif (b + v[2] - 1) > (u - 1):
                        tail = b + v[2] - 1 - u + 1 - 1
                        if tail <= y:
                            MOVES1 = y - (b + v[2] - 1)
                            MOVES2 = u - MOVES1
                            if min(MOVES1, MOVES2) <= minh:
                                minh = min(MOVES1, MOVES2)
                        elif tail > y:
                            MOVES1 = (b + v[2] - 1) - y
                            MOVES2 = u - MOVES1
                            if min(MOVES1, MOVES2) <= minh:
                                minh = min(MOVES1, MOVES2)                
                            
    return minh            
                    

def rushhour_goal_fn(state):
#IMPLEMENT
    '''Have we reached a goal state'''
    (u, w) = state.board_size
    for v in state.vehicle:
        if v[4]:
            (a, b) = v[1]
            (x, y) = state.goal_entrance            
            if not v[3]:
                if state.goal_orientation == 'N':
                    if y == b:
                        return True
                    else:
                        return False
                elif state.goal_orientation == 'S':
                    if y == 0:
                        if b == w - 1 - (v[2] - 2):
                            return True
                        else:
                            return False
                    else:
                        if y == b + v[2] - 1:
                            return True
                        else:
                            return False
                else:
                    return False
                
            if v[3]:
                if state.goal_orientation == 'W':
                    if x == a:
                        return True
                    else:
                        return False
                                     
                elif state.goal_orientation == 'E':
                    if x == 0:
                        if a == u - 1 - (v[2] - 2):
                            return True
                        else:
                            return False
                    else:
                        if x == a + v[2] - 1:
                            return True
                        else:
                            return False                
                else: 
                    return False


def make_init_state(board_size, vehicle_list, goal_entrance, goal_direction):
#IMPLEMENT
    '''Input the following items which specify a state and return a rushhour object
       representing this initial state.
         The state's its g-value is zero
         The state's parent is None
         The state's action is the dummy action "START"
       board_size = (m, n)
          m is the number of rows in the board
          n is the number of columns in the board
       vehicle_list = [v1, v2, ..., vk]
          a list of vehicles. Each vehicle vi is itself a list
          vi = [vehicle_name, (x, y), length, is_horizontal, is_goal] where
              vehicle_name is the name of the vehicle (string)
              (x,y) is the location of that vehicle (int, int)
              length is the length of that vehicle (int)
              is_horizontal is whether the vehicle is horizontal (Boolean)
              is_goal is whether the vehicle is a goal vehicle (Boolean)
      goal_entrance is the coordinates of the entrance tile to the goal and
      goal_direction is the orientation of the goal ('N', 'E', 'S', 'W')

   NOTE: for simplicity you may assume that
         (a) no vehicle name is repeated
         (b) all locations are integer pairs (x,y) where 0<=x<=n-1 and 0<=y<=m-1
         (c) vehicle lengths are positive integers
    '''
    x = rushhour("START", 0, None, vehicle_list, board_size, goal_entrance, goal_direction)
    return x
    

########################################################
#   Functions provided so that you can more easily     #
#   Test your implementation                           #
########################################################


def get_board(vehicle_statuses, board_properties):
    #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
    #and in generating sample trace output.
    #Note that if you implement the "get" routines
    #(rushhour.get_vehicle_statuses() and rushhour.get_board_size())
    #properly, this function should work irrespective of how you represent
    #your state.
    (m, n) = board_properties[0]
    board = [list(['.'] * n) for i in range(m)]
    for vs in vehicle_statuses:
        for i in range(vs[2]):  # vehicle length
            if vs[3]:
                # vehicle is horizontal
                board[vs[1][1]][(vs[1][0] + i) % n] = vs[0][0]
                # represent vehicle as first character of its name
            else:
                # vehicle is vertical
                board[(vs[1][1] + i) % m][vs[1][0]] = vs[0][0]
                # represent vehicle as first character of its name
    # print goal
    board[board_properties[1][1]][board_properties[1][0]] = board_properties[2]
    return board


def make_rand_init_state(nvehicles, board_size):
    '''Generate a random initial state containing
       nvehicles = number of vehicles
       board_size = (m,n) size of board
       Warning: may take a long time if the vehicles nearly
       fill the entire board. May run forever if finding
       a configuration is infeasible. Also will not work any
       vehicle name starts with a period.

       You may want to expand this function to create test cases.
    '''

    (m, n) = board_size
    vehicle_list = []
    board_properties = [board_size, None, None]
    for i in range(nvehicles):
        if i == 0:
            # make the goal vehicle and goal
            x = randint(0, n - 1)
            y = randint(0, m - 1)
            is_horizontal = True if randint(0, 1) else False
            vehicle_list.append(['gv', (x, y), 2, is_horizontal, True])
            if is_horizontal:
                board_properties[1] = ((x + n // 2 + 1) % n, y)
                board_properties[2] = 'W' if randint(0, 1) else 'E'
            else:
                board_properties[1] = (x, (y + m // 2 + 1) % m)
                board_properties[2] = 'N' if randint(0, 1) else 'S'
        else:
            board = get_board(vehicle_list, board_properties)
            conflict = True
            while conflict:
                x = randint(0, n - 1)
                y = randint(0, m - 1)
                is_horizontal = True if randint(0, 1) else False
                length = randint(2, 3)
                conflict = False
                for j in range(length):  # vehicle length
                    if is_horizontal:
                        if board[y][(x + j) % n] != '.':
                            conflict = True
                            break
                    else:
                        if board[(y + j) % m][x] != '.':
                            conflict = True
                            break
            vehicle_list.append([str(i), (x, y), length, is_horizontal, False])

    return make_init_state(board_size, vehicle_list, board_properties[1], board_properties[2])


def test(nvehicles, board_size):
    s0 = make_rand_init_state(nvehicles, board_size)
    se = SearchEngine('astar', 'full')
    #se.trace_on(2)
    final = se.search(s0, rushhour_goal_fn, heur_min_moves)