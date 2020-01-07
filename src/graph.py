import pynauty as nauty
import igraph as igraph
import colorsys as colorsys


class Graph(object):

    def __init__(self, numVertices=0, numVariables=None):
        self.iGraph = igraph.Graph(numVertices)
        self.iGraph.vs["label"] = [i for i in range(0, numVertices)]
        self.nautyGraph = nauty.Graph(numVertices)
        self.weights = {}
        self.numVariables = numVariables

    def __str__(self):
        return self.iGraph.__str__() + "\n" + self.nautyGraph.__str__()

    def add_edges(self, vertexPairs, weights=None):
        #    if (weights == None):
        self.iGraph.add_edges(vertexPairs)
        weightSet = set()
        for i in range(0, len(vertexPairs)):
            vertexPair = vertexPairs[i]
            self.nautyGraph.connect_vertex(vertexPair[0], vertexPair[1])
            if (weights != None):
                self.iGraph.es.select(
                    _source=vertexPair[0],
                    _target=vertexPair[1])["weight"] = weights[i]

                self.iGraph.es.select(
                    _source=vertexPair[0],
                    _target=vertexPair[1])["label"] = weights[i]
                weightSet.add(weights[i])

        distinctWeights = list(weightSet)

    # A list of disjoint sets of vertices representing a partition of the vertex set;
    # vertices not listed are placed into a single additional part
    def colour_vertices(self, vertexColouring):
        N = len(vertexColouring)
        colour_pallete = self.get_n_colours(len(vertexColouring))
        colours = [None] * len(self.iGraph.vs)
        i = 0

        for i in range(len(vertexColouring)):
            for vertex in list(vertexColouring[i]):
                colours[vertex] = colour_pallete[i]

        self.iGraph.vs["color"] = colours

    #    self.nautyGraph.set_vertex_coloring(vertexColouring)

    def get_n_colours(self, N):
        HSV_tuples = [(x * 1.0 / N, 0.5, 0.5) for x in range(N)]
        hex_out = []
        for rgb in HSV_tuples:
            rgb = map(lambda x: int(x * 255), colorsys.hsv_to_rgb(*rgb))
            hex_out.append('#%02x%02x%02x' % tuple(rgb))
        return hex_out

    def plot(self, *args, **kwargs):
        igraph.plot(self.iGraph, *args, **kwargs)

    def set_attributes(self, name, val, start, length):
        self.iGraph.vs[start:start + length][name] = val

    def automorphismGroup(self):
        return nauty.autgrp(self.nautyGraph)

    # Translates an edge-weighted bipartite graph into a vertex coloured
    # graph with the same automorphism group
    # def originalEdgeWeightedToVertexColoured(self):
    # TODO: Clean this up
    # TODO: Implement the more efficient version of this
    def getUnweightedNautyGraph(self):
        distinctWeights = {}
        adjacencyDict = {}
        vertexColours = {}
        numVertices = len(self.iGraph.vs)  # TODO: There must be a better way of getting this

        for vertexPair in self.iGraph.get_edgelist():
            edge = self.iGraph.es.select(
                _source=vertexPair[0],
                _target=vertexPair[1])  # TODO: make this safer

            minV = min(vertexPair)
            maxV = max(vertexPair)

            weight = edge["weight"][0]
            if (weight != 1):  # Even if weight is equal to 1??? Does it mattr
                # Could move this around and avoid a bit of duplication?
                if (weight in distinctWeights):
                    distinctWeights[weight].add(numVertices)
                else:
                    distinctWeights[weight] = set()
                    distinctWeights[weight].add(numVertices)

                adjacencyDict[minV].append(numVertices)
                if (maxV in adjacencyDict):
                    adjacencyDict[maxV].append(numVertices)
                else:
                    adjacencyDict[maxV] = [numVertices]
                numVertices += 1
            else:
                if (minV in adjacencyDict):
                    adjacencyDict[minV].append(maxV)
                else:
                    adjacencyDict[minV] = [maxV]

        for i in range(0, len(self.iGraph.vs)):
            colour = self.iGraph.vs[i]["color"]
            if colour in vertexColours:
                vertexColours[colour].add(i)
            else:
                vertexColours[colour] = {i}

        colourings = list(vertexColours.values())
        colourings.extend(list(distinctWeights.values()))

        # Now setting edge colours as well - This is quite ugly to be doing here
        distinctWeightsList = list(distinctWeights)
        colour_pallete = self.get_n_colours(len(distinctWeightsList))
        for i in range(0, len(self.iGraph.es)):
            if (self.iGraph.es[i]["weight"] != 1):
                self.iGraph.es[i]["color"] = colour_pallete[distinctWeightsList.index(self.iGraph.es[i]["weight"])]

        # This should really be cleaned up!
        g = nauty.Graph(numVertices,
                        False,
                        adjacency_dict=adjacencyDict,
                        vertex_coloring=colourings)
        self.nautyGraph = g
        return g

    def get_edgelist(self):
        return self.iGraph.get_edgelist()

    def get_orbital_partition(self, numVariables=None):
        automorphismGroup = self.automorphismGroup()
        generators = automorphismGroup[0]
        all_permutations = perms.generate_all(generators)
        if (numVariables == None):
            return perms.partitions(all_permutations, self.numVariables)
        else:
            return perms.partitions(all_permutations, numVariables)
