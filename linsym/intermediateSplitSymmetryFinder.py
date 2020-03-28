# A class that takes a linear program ad finds its symmetry group using an itermediate node method
from linsym import intermediateEqSymmetryFinder
from linsym import intermediateIneqSymmetryFinder


def findSymmetries(linProblem):
    # find the symmetries of the eq and ineq separately then take the max index
    hasEqComponent = len(linProblem.beq) > 0
    hasIneqComponent = len(linProblem.bineq) > 0

    if hasEqComponent and hasIneqComponent:

        symEq = intermediateEqSymmetryFinder.findSymmetries(linProblem)
        symIneq = intermediateIneqSymmetryFinder.findSymmetries(linProblem)

        d = {}
        c = 0
        sym = []
        # TODO[michaelr]: Could do an enumerate here?
        for i, j in zip(symEq, symIneq):
            if (i, j) not in d:
                d[(i, j)] = c
            sym.append(d[(i, j)])
            c += 1

        return sym
    elif hasEqComponent:
        return intermediateEqSymmetryFinder.findSymmetries(linProblem)
    elif hasIneqComponent:
        return intermediateIneqSymmetryFinder.findSymmetries(linProblem)
    else:
        # Could also return [] here, doesn't really matter
        raise Exception("Cannot find the symmetry of an empty linear problem")
