from unittest import TestCase
import intermediateIneqSymmetryFinder as sfIneq
from testUtils import *


class TestIntermediateSymmetryFinder(TestCase):
    objectiveTest = [1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1]

    def test_simpleUnweightedMatrixOnly(self):
        Aineq = listToSparseMatrix(constraintMatrix)
        linProblem = constructIneqMatrixOnlyLinProblem(Aineq)
        sym = sfIneq.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 2, 2, 2, 6, 7, 7, 7, 7, 11, 11])

    def test_simpleWeightedMatrixOnly(self):
        Aineq = listToSparseMatrix(weightedConstraintMatrix)
        linProblem = constructIneqMatrixOnlyLinProblem(Aineq)
        sym = sfIneq.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 3, 2, 3, 6, 7, 8, 7, 8, 11, 11, 13, 13, 15, 16, 15, 16])

    def test_largerUnweightedMatrixOnly(self):
        Aineq = listToSparseMatrix(largerConstraintMatrix)
        linProblem = constructIneqMatrixOnlyLinProblem(Aineq)
        sym = sfIneq.findSymmetries(linProblem)
        self.assertEqual(sym,
                         [0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 12, 12, 14, 14, 12, 14, 14, 12, 14, 14, 14, 14, 24, 24,
                          24, 24])

    def test_largerWeightedMatrixOnly(self):
        Aineq = listToSparseMatrix(largerWeightedConstraintMatrix)
        linProblem = constructIneqMatrixOnlyLinProblem(Aineq)
        sym = sfIneq.findSymmetries(linProblem)
        self.assertEqual(sym,
                         [0, 1, 0, 1, 4, 4, 6, 6, 4, 4, 6, 6, 12, 12, 14, 14, 12, 17, 17, 12, 14, 14, 17, 17, 24, 25,
                          24, 25, 28, 28, 28, 28])

    def test_simpleUnweightedMatrixWithSimpleObjFunc(self):
        Aineq = listToSparseMatrix(constraintMatrix)
        linProblem = constructIneqMatrixOnlyLinProblem(Aineq)
        linProblem.f = np.array([1, 1, 2, 1, 2, 1])
        sym = sfIneq.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 3, 2, 3, 6, 7, 8, 7, 8, 11, 11])

    def test_simpleUnweightedMatrixWithLowerBounds(self):
        Aineq = listToSparseMatrix(constraintMatrix)
        linProblem = constructIneqMatrixOnlyLinProblem(Aineq)
        linProblem.lb = np.array([1, 1, 2, 1, 2, 1])
        sym = sfIneq.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 3, 2, 3, 6, 7, 8, 7, 8, 11, 11])

    def test_simpleUnweightedMatrixWithUpperBounds(self):
        Aineq = listToSparseMatrix(constraintMatrix)
        linProblem = constructIneqMatrixOnlyLinProblem(Aineq)
        linProblem.ub = np.array([1, 1, 2, 1, 2, 1])
        sym = sfIneq.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 3, 2, 3, 6, 7, 8, 7, 8, 11, 11])

    def test_simpleUnweightedMatrixWithBeq(self):
        Aineq = listToSparseMatrix(constraintMatrix)
        linProblem = constructIneqMatrixOnlyLinProblem(Aineq)
        linProblem.bineq = np.array([1, 1, 2, 1, 2, 1, 1])
        sym = sfIneq.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 3, 2, 3, 6, 7, 8, 7, 8, 11, 11])

    def test_fullLinearProblem(self):
        Aineq = listToSparseMatrix(largerConstraintMatrix)
        linProblem = constructIneqMatrixOnlyLinProblem(Aineq)
        linProblem.bineq = np.array([1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1])
        # TODO[michaelr]: Shouldn't this be on lb and one ub????
        linProblem.lb = np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0])
        linProblem.lb = np.array([1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1])
        sym = sfIneq.findSymmetries(linProblem)
        self.assertEqual(sym,
                         [0, 1, 0, 1, 4, 5, 6, 7, 5, 4, 6, 7, 12, 12, 14, 15, 12, 17, 18, 12, 15, 14, 17, 18, 24, 25,
                          24, 25])
