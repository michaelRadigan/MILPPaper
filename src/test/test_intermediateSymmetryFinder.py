from unittest import TestCase
from linearProblem import LinearProblem
import numpy as np
from scipy.sparse import csr_matrix
import intermediateSymmetryFinder as sf


def constructMatrixOnlyLinProblem(A):
    beq = np.array([[1] for _ in range(A.shape[0])])

    # TODO[michaelr]: Clearly this is wrong but just making it work with what we already have...
    f = np.array([[1] for _ in range(A.shape[1])])
    intcon = np.array([[1] for _ in range(A.shape[1])])
    lb = np.array([[1] for _ in range(A.shape[1])])
    ub = np.array([[1] for _ in range(A.shape[1])])

    # TODO[michaelr]: Fx this! We are currently passing in eq to ineq to get around the awful design
    return LinearProblem(A, A, beq, beq, f, lb, ub)


def listToSparseMatrix(matrix):
    return csr_matrix([np.array(x) for x in matrix]).tocoo()


class TestIntermediateSymmetryFinder(TestCase):
    constraintMatrix = [
        [1, 1, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0],
        [1, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 1],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 1],
    ]

    weightedConstraintMatrix = [
        [1, 1, 0, 0, 0, 0],
        [1, 0, 3, 0, 0, 0],
        [1, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 3, 0],
        [0, 1, 0, 0, 0, 1],
        [0, 0, 2, 2, 0, 0],
        [0, 0, 0, 0, 2, 2],
    ]

    largerConstraintMatrix = [
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    ]

    largerWeightedConstraintMatrix = [
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
    ]

    objectiveTest = [1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1]

    # TODO[michaelr] Do we actually care about the orbits of the constraints?

    def test_simpleUnweightedMatrixOnly(self):
        Aeq = listToSparseMatrix(self.constraintMatrix)
        linProblem = constructMatrixOnlyLinProblem(Aeq)
        sym = sf.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 2, 2, 2, 6, 7, 7, 7, 7, 11, 11])

    def test_simpleWeightedMatrixOnly(self):
        Aeq = listToSparseMatrix(self.weightedConstraintMatrix)
        linProblem = constructMatrixOnlyLinProblem(Aeq)
        sym = sf.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 3, 2, 3, 6, 7, 8, 7, 8, 11, 11, 13, 13, 15, 16, 15, 16])

    def test_largerUnweightedMatrixOnly(self):
        Aeq = listToSparseMatrix(self.largerConstraintMatrix)
        linProblem = constructMatrixOnlyLinProblem(Aeq)
        sym = sf.findSymmetries(linProblem)
        self.assertEqual(sym,
                         [0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 12, 12, 14, 14, 12, 14, 14, 12, 14, 14, 14, 14, 24, 24,
                          24, 24])

    def test_largerWeightedMatrixOnly(self):
        Aeq = listToSparseMatrix(self.largerWeightedConstraintMatrix)
        linProblem = constructMatrixOnlyLinProblem(Aeq)
        sym = sf.findSymmetries(linProblem)
        self.assertEqual(sym,
                         [0, 1, 0, 1, 4, 4, 6, 6, 4, 4, 6, 6, 12, 12, 14, 14, 12, 17, 17, 12, 14, 14, 17, 17, 24, 25,
                          24, 25, 28, 28, 28, 28])

    def test_simpleUnweightedMatrixWithSimpleObjFunc(self):
        Aeq = listToSparseMatrix(self.constraintMatrix)
        linProblem = constructMatrixOnlyLinProblem(Aeq)
        linProblem.f = np.array([[1], [1], [2], [1], [2], [1]])
        sym = sf.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 3, 2, 3, 6, 7, 8, 7, 8, 11, 11])

    def test_simpleUnweightedMatrixWithLowerBounds(self):
        Aeq = listToSparseMatrix(self.constraintMatrix)
        linProblem = constructMatrixOnlyLinProblem(Aeq)
        linProblem.lb = np.array([[1], [1], [2], [1], [2], [1]])
        sym = sf.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 3, 2, 3, 6, 7, 8, 7, 8, 11, 11])

    def test_simpleUnweightedMatrixWithUpperBounds(self):
        Aeq = listToSparseMatrix(self.constraintMatrix)
        linProblem = constructMatrixOnlyLinProblem(Aeq)
        linProblem.ub = np.array([[1], [1], [2], [1], [2], [1]])
        sym = sf.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 3, 2, 3, 6, 7, 8, 7, 8, 11, 11])

    # TODO[michaelr]: I think that this is right but really double check this!
    def test_simpleUnweightedMatrixWithBeq(self):
        Aeq = listToSparseMatrix(self.constraintMatrix)
        linProblem = constructMatrixOnlyLinProblem(Aeq)
        linProblem.beq = np.array([[1], [1], [2], [1], [2], [1], [1]])
        sym = sf.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 3, 2, 3, 6, 7, 8, 7, 8, 11, 11])


