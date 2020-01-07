# Find orbital partition in the linear case
import pynauty as nauty
from collections import defaultdict
import pickle as pickle

problem = pickle.load(open("pickle/enlight16.p", "rb"))
ASparse = problem.Aeq
A = ASparse.toarray()
print('-1 mode')
numConstraints = len(A)
numVars = len(A[0])

values = defaultdict(set)
adjacencyDict = defaultdict(list)

nextIndex = numConstraints + numVars

Acoo = ASparse.tocoo()
coalesceDict = {}

for i, j, weight in zip(Acoo.row, Acoo.col, Acoo.data):
    if weight == 1:
        adjacencyDict[j].append(i + numVars)
    elif (j, weight) in coalesceDict:
        # The intermediate node already exists, just connect things up
        intermediateNodeIndex = coalesceDict[(j, weight)]
        adjacencyDict[i + numVars].append(intermediateNodeIndex)
    else:
        # Create an intermediate node and attach it up
        coalesceDict[(j, weight)] = nextIndex
        values[weight].add(nextIndex)
        adjacencyDict[j].append(nextIndex)
        adjacencyDict[i + numVars].append(nextIndex)
        nextIndex += 1

numVertices = nextIndex

# Colouring the variables by their values in f and their bounds
varColourings = defaultdict(set)
for i in range(len(problem.f)):
    f_i = problem.f[i][0]
    lb_i = problem.lb[i][0]
    ub_i = problem.ub[i][0]
    varColourings[(f_i, lb_i, ub_i)].add(i)

# Colouring constraints by their values in b
constraintsColourings = defaultdict(set)
for i in range(len(problem.beq)):
    constraintsColourings[problem.beq[i][0]].add(numVars + i)

colours = []
colours.extend(varColourings.values())
colours.extend(constraintsColourings.values())
#colours.extend([set(range(numVars))])
#colours.extend([set(range(numVars, numVars + numConstraints))])
colours.extend([set(l) for l in values.values()])

print(varColourings.values())
print(constraintsColourings.values())

# print(adjacencyDict)

bi = nauty.Graph(numVertices, False, adjacencyDict, colours)

print('About to find automorphism group')
autoGroup = nauty.autgrp(bi)
print(autoGroup[3])

symmetries = autoGroup[3]

print(symmetries)

# This is just a nice way to illustrate the symmetries in the enlight instances
#for i in range(16):
#    print('\setrowcoloured', end = ' ')
#    for j in range(16):
#        #print('{:4}'.format(symmetries[i*16 + j]), end = " ")
#        print('{' + str(symmetries[i*16 + j]), end = '}')
#    print(" ")


"""
# Creating a graph to view the problem
#g = ig.Graph(numVertices)
#g.vs["label"] = [i for i in range(0, numVertices)]
#edges = [(k, v) for (k, vs) in adjacencyDict.items() for v in vs]
#g.add_edges(edges)
#g.layout("drl")
#visualStyle = {'vertex_size': 10}
#print(g)
#ig.plot(g, **visualStyle)
"""