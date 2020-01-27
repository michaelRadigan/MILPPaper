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


def getVertexColouring(linProblem, values):
    vertexColouring = []
    vertexColouring.extend(getVariableColouring(linProblem.f, linProblem.lb, linProblem.ub))
    vertexColouring.extend(getConstraintColouring(linProblem.bineq, linProblem.numVarsIneq))
    vertexColouring.extend(values.values())
    return vertexColouring


# TODO[michaelr]: The return type of this method is ridiculous, wtf
def constructGraphIntermediate(linProblem):
    numConstraints = linProblem.Aineq.shape[0]
    if numConstraints == 0:
        return None
    numVars = linProblem.numVarsIneq
    numVertices = numConstraints + numVars

    intermediateNodeColouring = defaultdict(set)
    adjacencyDict = defaultdict(list)
    coalesceDict = {}

    for i, j, weight in zip(linProblem.Aineq.row, linProblem.Aineq.col, linProblem.Aineq.data):

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

    vertexColouring = getVertexColouring(linProblem, intermediateNodeColouring)
    return nauty.Graph(numVertices, False, adjacencyDict, vertexColouring), vertexColouring


def findSymmetries(linProblem):
    graph = constructGraphIntermediate(linProblem)[0]
    aut = nauty.autgrp(graph)[3]
    return aut