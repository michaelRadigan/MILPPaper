# A class representing a linear program
from collections import defaultdict
import pynauty as nauty
import time as time
import math as math


def combineLayers(layers, numVertices):
    combinedLayers = defaultdict(list)
    for i, layer in enumerate(layers):
        for startNode, edges in layer.items():
            for edge in edges:
                endNode = edge[0]
                combinedLayers[startNode + i * numVertices].append(endNode + i * numVertices)
    return combinedLayers



# TODO[michaelr]: intcon is not used, can we just nuke it (will it break the pickled stuff?
class LinearProblem(object):
    def __init__(self, Aeq, Aineq, beq, bineq, f, lb, ub):
        self.Aeq = Aeq.tocoo()
        self.Aineq = Aineq.tocoo()
        self.beq = beq
        self.bineq = bineq
        self.f = f
        self.lb = lb
        self.ub = ub
        # TODO[michaelr]: This looks a bit shit, surely we can do better?
        self.eqGraphIntermediate = None
        self.ineqGraphIntermediate = None
        self.eqGraphSuperposition = None
        self.ineqGraphSuperposition = None
        self.eqPartitionSuperposition = None
        self.ineqPartitionSuperposition = None
        self.eqPartitionIntermediate = None
        self.ineqPartitionIntermediate = None

        # TODO[michaelr]: This looks a bit shit, surely we can do better?
        if len(beq) != 0:
            self.numVarsEq = Aeq.shape[1]
            self.eqGraphIntermediate, self.eqPartitionIntermediate = self.constructGraphIntermediate(Aeq, beq)
            self.eqGraphSuperposition, self.eqPartitionSuperposition = self.constructGraphSuperposition(Aeq, beq)
        # TODO[michaelr]: This looks a bit shit, surely we can do better?
        if len(bineq) != 0:
            self.numVarsIneq = Aineq.shape[1]
            self.ineqGraphIntermediate, self.ineqPartitionIntermediate = self.constructGraphIntermediate(Aineq, bineq)
            self.ineqGraphSuperposition, self.ineqPartitionSuperposition = self.constructGraphSuperposition(Aineq, bineq)

    # TODO[michaelr]: The return type of this method is ridiculous, wtf
    def constructGraphIntermediate(self, A, b):
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

        vertexColouring = self.getVertexColouring(b, numVars, intermediateNodeColouring)
        return nauty.Graph(numVertices, False, adjacencyDict, vertexColouring), vertexColouring

    def getVertexColouring(self, b, numVars, values):
        vertexColouring = []
        vertexColouring.extend(self.getVariableColouring())
        vertexColouring.extend(self.getConstraintColouring(b, numVars))
        vertexColouring.extend(values.values())
        return vertexColouring

    def getVariableColouring(self):
        varColourings = defaultdict(set)
        for i in range(len(self.f)):
            f_i = self.f[i][0]
            lb_i = self.lb[i][0]
            ub_i = self.ub[i][0]
            varColourings[(f_i, lb_i, ub_i)].add(i)
        return varColourings.values()

    @staticmethod
    def getConstraintColouring(b, numVars):
        constraintColourings = defaultdict(set)
        for i in range(len(b)):
            constraintColourings[b[i][0]].add(numVars + i)
        return constraintColourings.values()

    def constructGraphSuperposition(self, A, b):
        numConstraints = A.shape[0]
        numVars = A.shape[1]

        adjacencyDict = defaultdict(set)
        distinctWeightsToBin = {}
        numDistinctWeights = 0

        for i, j, weight in zip(A.row, A.col, A.data):
            adjacencyDict[j].add((i + numVars, weight))
            if weight not in distinctWeightsToBin:
                distinctWeightsToBin[weight] = numDistinctWeights + 1
                numDistinctWeights += 1

        layers = []
        numLayers = int(math.floor(math.log2(len(distinctWeightsToBin))) + 1)
        for k in range(numLayers):
            layer_k = self.constructSuperpositionLayer(distinctWeightsToBin, k, numVars, A)
            layers.append(layer_k)

        numVertices = numVars + numConstraints
        superposedAdjacencyDict = combineLayers(layers, numVertices)

        singleLayerVariableColourings = self.getVariableColouring()
        singleLayerConstraintColourings = self.getConstraintColouring(b, numVars)

        colourings = []
        colourings.extend(singleLayerVariableColourings)
        colourings.extend(singleLayerConstraintColourings)
        for i in range(1, numLayers):
            for variableColouring in singleLayerVariableColourings:
                colourings.append(set(map(lambda x: x + i*numVertices, variableColouring)))
            for constraintColouring in singleLayerConstraintColourings:
                colourings.append(set(map(lambda x: x + i*numVertices, constraintColouring)))

        colourings.sort(key=max)

        # Then construct graph with the adjacencyDict and the colourings
        return nauty.Graph(numLayers*numVertices, False, superposedAdjacencyDict, colourings), colourings

    def constructSuperpositionLayer(self, weights, k, numVars, A):
        # TODO: Why does this need access to A?
        # TODO: Should this not construct straight from the bipartite graph?
        layer_k = defaultdict(list)
        for i, j, weight in zip(A.row, A.col, A.data):
            if self.shouldIncludeEdge(weight, k, weights):
                layer_k[j].append((i + numVars, weight))
        return layer_k

    # TODO[michaelr]: This is both mental and shit :(

    @staticmethod
    def shouldIncludeEdge(colour, i, distinctWeights):
        binaryMapping = distinctWeights[colour]
        return (binaryMapping >> i) & 1

    def findEqSymmetriesSuperposition(self):
        if self.eqGraphSuperposition is None:
            return 0, None
        start = time.process_time()
        orbits = nauty.autgrp(self.eqGraphSuperposition)[3][0:self.numVarsEq]
        end = time.process_time()
        print("Superposition took: " + str(end - start))
        print(end - start)
        return end - start, orbits

    def findEqSymmetriesIntermediate(self):
        if self.eqGraphIntermediate is None:
            return 0, None
        start = time.process_time()
        orbits = nauty.autgrp(self.eqGraphIntermediate)[3][0:self.numVarsEq]
        end = time.process_time()
        print("Intermediate took: " + str(end - start))
        return end - start, orbits

    def findIneqSymmetriesIntermediate(self):
        if self.ineqGraphIntermediate is None:
            return 0, None
        start = time.process_time()
        orbits = nauty.autgrp(self.ineqGraphIntermediate)[3][0:self.numVarsIneq]
        end = time.process_time()
        print("Intermediate took: " + str(end - start))
        return end - start, orbits

    def findIneqSymmetriesSuperposition(self):
        if self.ineqGraphSuperposition is None:
            return 0, None
        start = time.process_time()
        orbits = nauty.autgrp(self.ineqGraphSuperposition)[3][0:self.numVarsIneq]
        end = time.process_time()
        print("Superposition took: " + str(end - start))
        return end - start, orbits
