# A class that takes a linear program and finds its symmetry group using an intermediate node method
from collections import defaultdict
import pynauty as nauty


def getVariableColouring(f, lb, ub):
    varColourings = defaultdict(set)
    for i in range(len(f)):
        f_i = f[i][0]
        lb_i = lb[i][0]
        ub_i = ub[i][0]
        varColourings[(f_i, lb_i, ub_i)].add(i)
    return varColourings.values()


def getConstraintColouring(b, numVars):
    constraintColourings = defaultdict(set)
    for i in range(len(b)):
        constraintColourings[b[i][0]].add(numVars + i)
    return constraintColourings.values()


# TODO[michaelr]: Just pass in the linProblem??
def getVertexColouring(b, numVars, values, f, lb, ub):
    vertexColouring = []
    vertexColouring.extend(getVariableColouring(f, lb, ub))
    vertexColouring.extend(getConstraintColouring(b, numVars))
    vertexColouring.extend(values.values())
    return vertexColouring


# TODO[michaelr]: The return type of this method is ridiculous, wtf
# TODO[michaelr]: Pass in the linProblem
def constructGraphIntermediate(A, b, f, lb, ub):
    numConstraints = A.shape[0]
    if numConstraints == 0:
        return None
    numVars = A.shape[1]
    numVertices = numConstraints + numVars

    intermediateNodeColouring = defaultdict(set)
    adjacencyDict = defaultdict(list)
    coalesceDict = {}

    for i, j, weight in zip(A.row, A.col, A.data):

        # TODO[michaelr]: This should not be 1, we can improve this by making the edge that does not
        # TODO[michaelr]: be the most common edge weight.
        if weight == 1:
            adjacencyDict[j].append(i + numVars)
        elif (j, weight) in coalesceDict:
            # The intermediate node already exists, just connect things up
            intermediateNodeIndex = coalesceDict[(j, weight)]
            adjacencyDict[i + numVars].append(intermediateNodeIndex)
        else:
            # Create an intermediate node and attach it up
            coalesceDict[(j, weight)] = numVertices
            intermediateNodeColouring[weight].add(numVertices)
            adjacencyDict[j].append(numVertices)
            adjacencyDict[i + numVars].append(numVertices)
            numVertices += 1

    vertexColouring = getVertexColouring(b, numVars, intermediateNodeColouring, f, lb, ub)
    return nauty.Graph(numVertices, False, adjacencyDict, vertexColouring), vertexColouring


# TODO[michaelr]: Clean everything such that this is less heinous
def findSymmetries(A, b, f, lb, ub):
    graph = constructGraphIntermediate(A, b, f, lb, ub)[0]
    return nauty.autgrp(graph)[3]
