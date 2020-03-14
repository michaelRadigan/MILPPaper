# A class that takes a linear program ad finds its symmetry group using an itermediate node method
from .intermediateEqSymmetryFinder import findSymmetries as findEqSymmetries
from .intermediateIneqSymmetryFinder import findSymmetries as findIneqSymmetries


def findSymmetries(linProblem):
    # find the symmetries of the eq and ineq separately then take the mae index
    symEq = findEqSymmetries(linProblem)
    symIneq = findIneqSymmetries(linProblem)

    d = {}
    c = 0
    sym = []
    for i, j in zip(symEq, symIneq):
        if (i, j) not in d:
            d[(i, j)] = c
            c += 1
        sym.append(d[(i, j)])

    return sym