#***********************************************************
#Symantics           					   *
#-----------                                               *
#untreatedStates = utStates , tStates = treated currStates,*
#up =  1, down = 2, left = 3, right = 4                    *
#nsma = number of the same move allowed                    *
#Cs 475 final project                                      *
#***********************************************************
import queue, numpy as np
from numpy import linalg as LA


#length = int(input("length?: "))
#k = int(input("k value?(must be even!): "))
k = 4
nsma = k - 3

def calculateSaw(matrix,walkLen):
   numStates = len(matrix)
   dfa_start_states = np.array([0], dtype=np.object) 
   dfa_final_states = [numStates - 1 ] 
   dfa_start_state_vector = np.zeros(numStates, dtype=np.object)
   dfa_final_state_vector = np.zeros((numStates, 1), dtype=np.object)
   dfa_start_state_vector[0] = 1
   for state in dfa_final_states:
       dfa_final_state_vector[state][0] = 1
   dfa_trans_mat = np.mat(matrix)
   dfa_start_mat = np.mat(dfa_start_state_vector)
   dfa_final_mat = np.mat(dfa_final_state_vector)

   # Calculates the DFA Transition Matrix to the 'length' power
   dfa_transition_matrix_exp = LA.matrix_power(dfa_trans_mat, walkLen)
   dfa_trans_exp_mat = np.mat(dfa_transition_matrix_exp)
   result = dfa_start_mat * dfa_trans_exp_mat * dfa_final_mat 
   number_result = result.item(0, 0) 
   final_result = pow(4, walkLen) - number_result
   print("For length: ", walkLen, "num of saw is ", final_result)

def transMatrix(dfaTable):
    numInputs = 4
    numStates = len(dfaTable) 
    dfa_transition_matrix = np.zeros((numStates, numStates), dtype=np.object)
    state_count = 0

    for values in dfaTable:
        for i in range(0, numInputs):
           dfa_transition_matrix[state_count][values[i]] += 1
        state_count += 1
    return dfa_transition_matrix

def getDist(u,v):
    #get vector v
    vec = [0,0]
    if (v == 1):
        vec[0] = 1
    if (v == 2):
        vec[0] = -1
    if (v == 3):
        vec[1] = -1
    if (v == 4):
        vec[1] = 1

    if(u == [3,3,1]):

    #get x and y values of u
    for i in range(0,len(u)):
        if (u[i] == 1):
            vec[0] = vec[0] + 1
        if (u[i] == 2):
            vec[0] = vec[0] + -1
        if (u[i] == 3):
            vec[1] = vec[1] + -1
        if (u[i] == 4):
            vec[1] = vec[1] + 1
    distance = ((vec[0])**2 + (vec[1])**2 )**.5
    return distance

#return 2: made a loop 
#return 0: didnt make a loop
def recursiveSteps(u,v):
    if(len(u) == k - 1):
        if(getDist(u,v) == 0):
            return 2
        return 0
    for i in range(1,5):
        augmentedWalk = u[:]
        agumentedWalk.append(v)
        recursiveSteps(augmentedWalk,i)

#returns 0 cant make a loop, 1 if can make a loop, 2 if it does make a loop
def checkMove(u,v):

    #check for backwards move
    val = (v - 1) % 2
    if ( (val == 1 and (v - 1== u[len(u)-1])) or (val == 0 and (v+1) == u[len(u)-1])):
        return 2

    #check if finished
    if(len(u) ==  k - 1):
        if(getDist(u,v) == 0):
            return 2
        return 0
    

def findNew(state):
    if(len(state) == 1):
        return tStates.index(state)

    if(checkMove(state[:-1], state[len(state) - 1]) == 1):
        if (state in tStates):
            return tStates.index(state)

        if(state in utStates.queue):
            return( (utStates.queue).index(state) + len(tStates))

        else:
            utStates.put(state)
            return (len(tStates) + utStates.qsize())
    else:
        state.pop(0)
        return findNew(state)
 
utStates,tStates,transfers,moves = (queue.Queue(),[], [], [1,2,3,4])
utStates.put([0])
while not utStates.empty():
    mem_k = utStates.get()
    tStates.append(mem_k)
    transition = []
    for i in moves:
        if mem_k[0] is 0:
            if (not [i] in tStates):
                utStates.put([i])
                transition.append(i)
        else:
            state = mem_k[:]
            state.append(i)
            if(checkMove(mem_k,i) == 1):
                if ((not state in tStates) or (not state in utStates.queue)):
                    utStates.put(state)
                    transition.append(len(tStates) + utStates.qsize() - 1)

            elif(checkMove(mem_k,i) == 0):
                transition.append(findNew(state))
            elif(checkMove(mem_k,i) == 2):
                transition.append(1000)
    transfers.append(transition)

for i in range(0, len(transfers)):
    for j in range(0,4):
        if(transfers[i][j] == 1000):
            transfers[i][j] = len(tStates) 
transfers.append([len(transfers) ,len(transfers) , len(transfers), len(transfers)])
tStates.append([])

#print ("\ntreated states")
print (tStates)
print ("\ntransfers")
print (transfers)
#print("number of states is", len(tStates))

for i in range (1,7):
    length = i
    calculateSaw(transMatrix(transfers),length)
