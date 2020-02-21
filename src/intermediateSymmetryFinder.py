# A class that takes a linear program and finds its symmetry group using an intermediate node method
from collections import defaultdict
import pynauty as nauty


def getVariableColouring(f, lb, ub):
    varColourings = defaultdict(set)
    for i in range(len(f)):
        f_i = f[i]
        lb_i = lb[i]
        ub_i = ub[i]
        varColourings[(f_i, lb_i, ub_i)].add(i)
    return varColourings.values()


def getConstraintColouring(b, numVars):
    constraintColourings = defaultdict(set)
    for i in range(len(b)):
        constraintColourings[b[i]].add(numVars + i)
    return constraintColourings.values()


def getVertexColouring(linProblem, values):
    vertexColouring = []
    vertexColouring.extend(getVariableColouring(linProblem.f, linProblem.lb, linProblem.ub))
    vertexColouring.extend(getConstraintColouring(linProblem.bineq, linProblem.numVars))
    vertexColouring.extend(values.values())
    return vertexColouring


def foo(linProblem):
    numVertices = linProblem.numConstraints + linProblem.numVars

    intermediateNodeColouring = defaultdict(set)
    adjacencyDict = defaultdict(list)

    # The coalesceDict
    coalesceDict = {}

    for iineq, jineq, weightineq, in zip(linProblem.Aineq.row, linProblem.Aineq.col, linProblem.Aineq.data):

        # TODO[michaelr]: This should not be 1, we can improve this by making the edge that does not
        # TODO[michaelr]: need an intermediate node be the most common edge weight.
        if weightineq == 1:
            adjacencyDict[jineq].append(iineq + linProblem.numVars)
        elif (jineq, weightineq) in coalesceDict:
            # The intermediate node already exists, just connect things up
            intermediateNodeIndex = coalesceDict[(jineq, weightineq)]
            adjacencyDict[iineq + linProblem.numVars].append(intermediateNodeIndex)
        else:
            # Create an intermediate node and attach it up
            coalesceDict[(jineq, weightineq)] = numVertices
            intermediateNodeColouring[weightineq].add(numVertices)
            adjacencyDict[jineq].append(numVertices)
            adjacencyDict[iineq + linProblem.numVars].append(numVertices)
            numVertices += 1

    # Resetting the coalesceDict as eq intermediate nodes can ever be coalesced with ineq
    # The coalesceDict
    coalesceDict = {}

    for i, j, weight in zip(linProblem.Aeq.row, linProblem.Aeq.col, linProblem.Aeq.data):
        # Can almost certainly clean this up a bit
        jeq = j + linProblem.numVarsIneq
        ieq = i + linProblem.numVarsIneq
        # TODO[michaelr]: This should not be 1, we can improve this by making the edge that does not
        # TODO[michaelr]: need an intermediate node be the most common edge weight.
        if weight == 1:
            adjacencyDict[jeq].append(ieq + linProblem.numVars)
        elif (jeq, weight) in coalesceDict:
            # The intermediate node already exists, just connect things up
            intermediateNodeIndex = coalesceDict[(jeq, weight)]
            adjacencyDict[ieq + linProblem.numVars].append(intermediateNodeIndex)
        else:
            # Create an intermediate node and attach it up
            coalesceDict[(jeq, weight)] = numVertices
            intermediateNodeColouring[weight].add(numVertices)
            adjacencyDict[jeq].append(numVertices)
            adjacencyDict[ieq + linProblem.numVars].append(numVertices)
            numVertices += 1

    return numVertices, intermediateNodeColouring, adjacencyDict


def constructGraphIntermediate(linProblem):
    if linProblem.numConstraints == 0 or linProblem.numVars == 0:
        raise ValueError("Can't construct a problem graph from an incomplete problem")

    numVertices, intermediateNodeColouring, adjacencyDict = foo(linProblem)

    vertexColouring = getVertexColouring(linProblem, intermediateNodeColouring)
    return nauty.Graph(numVertices, False, adjacencyDict, vertexColouring)


def findSymmetries(linProblem):
    graph = constructGraphIntermediate(linProblem)
    aut = nauty.autgrp(graph)[3]
    return aut
