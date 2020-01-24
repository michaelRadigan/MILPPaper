from unittest import TestCase
from linearProblem import LinearProblem
import numpy as np
from scipy.sparse import csr_matrix
import intermediateIneqSymmetryFinder as sfIneq
import random as rand


def constructMatrixOnlyLinProblem(A):
    beq = randArray(A.shape[1])
    bineq = np.array([[1] for _ in range(A.shape[0])])

    # TODO[michaelr]: Clearly this is wrong but just making it work with what we already have...
    f = np.array([[1] for _ in range(A.shape[1])])
    lb = np.array([[1] for _ in range(A.shape[1])])
    ub = np.array([[1] for _ in range(A.shape[1])])

    Aeq = randMatrix(A.shape[1], A.shape[0])

    # TODO[michaelr]: Fx this! We are currently passing in eq to ineq to get around the awful design
    return LinearProblem(Aeq, A, beq, bineq, f, lb, ub)


def randMatrix(n, m):
    gen = rand.Random()
    matrix = [[gen.randint(0, 256) for _ in range(n)] for _ in range(m)]
    return listToSparseMatrix(matrix)


def randArray(n):
    gen = rand.Random()
    return np.array([[gen.randint(0, 256)] for _ in range(n)])


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
        Aineq = listToSparseMatrix(self.constraintMatrix)
        linProblem = constructMatrixOnlyLinProblem(Aineq)
        sym = sfIneq.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 2, 2, 2, 6, 7, 7, 7, 7, 11, 11])

    def test_simpleWeightedMatrixOnly(self):
        Aineq = listToSparseMatrix(self.weightedConstraintMatrix)
        linProblem = constructMatrixOnlyLinProblem(Aineq)
        sym = sfIneq.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 3, 2, 3, 6, 7, 8, 7, 8, 11, 11, 13, 13, 15, 16, 15, 16])

    def test_largerUnweightedMatrixOnly(self):
        Aineq = listToSparseMatrix(self.largerConstraintMatrix)
        linProblem = constructMatrixOnlyLinProblem(Aineq)
        sym = sfIneq.findSymmetries(linProblem)
        self.assertEqual(sym,
                         [0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 12, 12, 14, 14, 12, 14, 14, 12, 14, 14, 14, 14, 24, 24,
                          24, 24])

    def test_largerWeightedMatrixOnly(self):
        Aineq = listToSparseMatrix(self.largerWeightedConstraintMatrix)
        linProblem = constructMatrixOnlyLinProblem(Aineq)
        sym = sfIneq.findSymmetries(linProblem)
        self.assertEqual(sym,
                         [0, 1, 0, 1, 4, 4, 6, 6, 4, 4, 6, 6, 12, 12, 14, 14, 12, 17, 17, 12, 14, 14, 17, 17, 24, 25,
                          24, 25, 28, 28, 28, 28])

    def test_simpleUnweightedMatrixWithSimpleObjFunc(self):
        Aineq = listToSparseMatrix(self.constraintMatrix)
        linProblem = constructMatrixOnlyLinProblem(Aineq)
        linProblem.f = np.array([[1], [1], [2], [1], [2], [1]])
        sym = sfIneq.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 3, 2, 3, 6, 7, 8, 7, 8, 11, 11])

    def test_simpleUnweightedMatrixWithLowerBounds(self):
        Aineq = listToSparseMatrix(self.constraintMatrix)
        linProblem = constructMatrixOnlyLinProblem(Aineq)
        linProblem.lb = np.array([[1], [1], [2], [1], [2], [1]])
        sym = sfIneq.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 3, 2, 3, 6, 7, 8, 7, 8, 11, 11])

    def test_simpleUnweightedMatrixWithUpperBounds(self):
        Aineq = listToSparseMatrix(self.constraintMatrix)
        linProblem = constructMatrixOnlyLinProblem(Aineq)
        linProblem.ub = np.array([[1], [1], [2], [1], [2], [1]])
        sym = sfIneq.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 3, 2, 3, 6, 7, 8, 7, 8, 11, 11])

    def test_simpleUnweightedMatrixWithBeq(self):
        Aineq = listToSparseMatrix(self.constraintMatrix)
        linProblem = constructMatrixOnlyLinProblem(Aineq)
        linProblem.bineq = np.array([[1], [1], [2], [1], [2], [1], [1]])
        sym = sfIneq.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 3, 2, 3, 6, 7, 8, 7, 8, 11, 11])

    def test_fullLinearProblem(self):
        Aineq = listToSparseMatrix(self.largerConstraintMatrix)
        linProblem = constructMatrixOnlyLinProblem(Aineq)
        linProblem.bineq = np.array([[1], [1], [1], [1], [1], [2], [1], [1], [1], [1], [2], [1], [1], [1], [1], [1]])
        # TODO[michaelr]: Shouldn't this be on lb and one ub????
        linProblem.lb = np.array([[0], [0], [0], [0], [1], [0], [0], [0], [0], [1], [0], [0]])
        linProblem.lb = np.array([[1], [1], [1], [1], [2], [1], [1], [1], [1], [2], [1], [1]])
        sym = sfIneq.findSymmetries(linProblem)
        self.assertEqual(sym,
                         [0, 1, 0, 1, 4, 5, 6, 7, 5, 4, 6, 7, 12, 12, 14, 15, 12, 17, 18, 12, 15, 14, 17, 18, 24, 25,
                          24, 25])
