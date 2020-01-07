import pynauty as nauty
import igraph as igraph
import colorsys as colorsys
import copy as copy
import graph as graph
import itertools as itertools

class SymmetryFinder(object):

  def __init__(self, constraintMatrix, Q=None, c=None, b=None):
    # Here we are making the assumption that the constraint matrix is well formed
    # TODO: Setting base obj here is likely cleaner
    print('a')
    self.graph = self.construct_graph(constraintMatrix)
    print('b')
    self.bi = self.construct_bi(constraintMatrix, Q, c, b)
    print('c')

  def equivalentQPartition(self, s, Q):
    length = len(Q)
    distincts = {}
    for x in range(length):
      distincts[x] = set([x])
    matched = set()
      
    for i, j in itertools.combinations(s,2):
      if i in matched:
        break;
      if (Q[i][i] == Q[j][j]):
        equal = True
        for p in range(length):
          if (p != i and p != j):
            if (not (Q[p][i] + Q[i][p] == Q[p][j] + Q[j][p])):
              equal = False
              break;

        if equal:
          distincts[i].add(j)          
          del distincts[j]
          matched.add(j)        

    return distincts
  
  # This graph only exist for packing problems??
  def construct_graph(self, constraintMatrix):
    numVars = len(constraintMatrix[0])
    g = graph.Graph(numVars)
    print("len is: " + str(len(constraintMatrix)))
    for i in range(0, len(constraintMatrix)):
      print(i)
      nonZeroes = []
      weights = []
      for j in range(0, len(constraintMatrix[0])):
        weight = constraintMatrix[i][j]
        if (weight != 0):
          nonZeroes.append(j)
          weights.append(weight)
      if (len(nonZeroes) != 0):
        pairs = [pair for pair in itertools.combinations(nonZeroes, 2)]
        hackWeights = [weights[0] for x in range(0, len(pairs))]
        g.add_edges(pairs, hackWeights)
    return g

  def normaliseA(self, A, b):
    zeros = set()
    normalisedA = list(A)
    for i in range(len(b)):
      val = b[i]
      if (val == 0):
        zeros.add(i)
      else:
        normalisedA[i] = [a/val for a in A[i]]
    return zeros, normalisedA
        
    
  # Should reimpliment this with the improvement from knowing that it is a bipartite graph
  def construct_bi(self, A, Q=None,c=None, b=None):
    numConstraints = len(A)
    numVars = len(A[0])
    zeros = set()

    if c == None:
      c = [1]*numVars
    if b != None:
      zeros, A = self.normaliseA(A, b)
    
    g = graph.Graph(numVars + numConstraints, numVars)
#    zeros, A = self.normaliseA(A, b)
    distinctObjDict = {}

    print("initialised")
    for i in range(numVars):
      val = (c[i], i in zeros)
      if (val in distinctObjDict):
        distinctObjDict[val].add(i) 
      else:
        distinctObjDict[val] = set()
        distinctObjDict[val].add(i)
        
    distincts = list(distinctObjDict.values())
    partitions = []
    if Q != None:
      print("Q is set")
      for distinctSet in distincts:
        partition = self.equivalentQPartition(distinctSet, Q)
        partitions.extend(partition)

    distincts.append(set(range(numVars, numVars + numConstraints)))
    g.colour_vertices(distincts)

    print("entering double loop")
    for i in range(0, numVars):
      print("i is: " + str(i))
      for j in range(0, numConstraints):
        weight = A[j][i]
        if (weight != 0):               
          g.add_edges([(i, numVars + j)], [weight])
    g.nautyGraph = g.getUnweightedNautyGraph()

    return g
  
  def get_symmetries(self):
    return self.bi.get_orbital_partition()


  
