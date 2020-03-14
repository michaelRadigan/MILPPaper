from unittest import TestCase
import numpy as np


from testUtils import listToSparseMatrix, constructDoubledMatrixOnlyLinProblem, constructIneqMatrixOnlyLinProblem, constructEqMatrixOnlyLinProblem
from testUtils import constraintMatrix, weightedConstraintMatrix, largerConstraintMatrix
from testUtils import largerWeightedConstraintMatrix
from linsym import intermediateSplitSymmetryFinder as sf
from linsym import linearProblem


class TestIntermediateSymmetryFinder(TestCase):
    objectiveTest = [1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1]

    # TODO[michaelr] Do we actually care about the orbits of the constraints?

    def test_simpleUnweightedMatrixOnly(self):
        Aeq = listToSparseMatrix(constraintMatrix)
        linProblem = constructDoubledMatrixOnlyLinProblem(Aeq)
        sym = sf.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 2, 2, 2, 6, 7, 7, 7, 7, 11, 11])

    def test_simpleWeightedMatrixOnly(self):
        Aeq = listToSparseMatrix(weightedConstraintMatrix)
        linProblem = constructDoubledMatrixOnlyLinProblem(Aeq)
        sym = sf.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 3, 2, 3, 6, 7, 8, 7, 8, 11, 11, 13, 13, 15, 16, 15, 16])

    def test_largerUnweightedMatrixOnly(self):
        Aeq = listToSparseMatrix(largerConstraintMatrix)
        linProblem = constructDoubledMatrixOnlyLinProblem(Aeq)
        sym = sf.findSymmetries(linProblem)
        self.assertEqual(sym,
                         [0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 12, 12, 14, 14, 12, 14, 14, 12, 14, 14, 14, 14, 24, 24,
                          24, 24])

    def test_largerWeightedMatrixOnly(self):
        Aeq = listToSparseMatrix(largerWeightedConstraintMatrix)
        linProblem = constructDoubledMatrixOnlyLinProblem(Aeq)
        sym = sf.findSymmetries(linProblem)
        self.assertEqual(sym,
                         [0, 1, 0, 1, 4, 4, 6, 6, 4, 4, 6, 6, 12, 12, 14, 14, 12, 17, 17, 12, 14, 14, 17, 17, 24, 25,
                          24, 25, 28, 28, 28, 28])

    def test_simpleUnweightedMatrixWithSimpleObjFunc(self):
        Aeq = listToSparseMatrix(constraintMatrix)
        linProblem = constructDoubledMatrixOnlyLinProblem(Aeq)
        linProblem.f = np.array([1, 1, 2, 1, 2, 1])
        sym = sf.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 3, 2, 3, 6, 7, 8, 7, 8, 11, 11])

    def test_simpleUnweightedMatrixWithLowerBounds(self):
        Aeq = listToSparseMatrix(constraintMatrix)
        linProblem = constructDoubledMatrixOnlyLinProblem(Aeq)
        linProblem.lb = np.array([1, 1, 2, 1, 2, 1])
        sym = sf.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 3, 2, 3, 6, 7, 8, 7, 8, 11, 11])

    def test_simpleUnweightedMatrixWithUpperBounds(self):
        Aeq = listToSparseMatrix(constraintMatrix)
        linProblem = constructDoubledMatrixOnlyLinProblem(Aeq)
        linProblem.ub = np.array([1, 1, 2, 1, 2, 1])
        sym = sf.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 3, 2, 3, 6, 7, 8, 7, 8, 11, 11])

    def test_simpleUnweightedMatrixWithBineq(self):
        Aeq = listToSparseMatrix(constraintMatrix)
        linProblem = constructDoubledMatrixOnlyLinProblem(Aeq)
        linProblem.bineq = np.array([1, 1, 2, 1, 2, 1, 1])
        sym = sf.findSymmetries(linProblem)
        self.assertEqual(sym, [0, 0, 2, 3, 2, 3, 6, 7, 8, 7, 8, 11, 11])

    def test_fullLinearProblem(self):
        Aeq = listToSparseMatrix(largerConstraintMatrix)
        linProblem = constructDoubledMatrixOnlyLinProblem(Aeq)
        linProblem.bineq = np.array([1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1])
        linProblem.lb = np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0])
        linProblem.lb = np.array([1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1])
        sym = sf.findSymmetries(linProblem)
        self.assertEqual(sym,
                         [0, 1, 0, 1, 4, 5, 6, 7, 5, 4, 6, 7, 12, 12, 14, 15, 12, 17, 18, 12, 15, 14, 17, 18, 24, 25,
                          24, 25])

    def test_simpleEqIneqSplit(self):
        Aeq = listToSparseMatrix(constraintMatrix)

        Aineq = listToSparseMatrix([[0, 0, 1, 0, 1, 0]])
        beq = np.ones(Aeq.shape[0])
        bineq = np.ones(Aineq.shape[0])
        f = np.ones(Aeq.shape[1])
        lb = np.ones(Aeq.shape[1])
        ub = np.ones(Aeq.shape[1])

        linProblem = linearProblem.LinearProblem(Aeq, Aineq, beq, bineq, f, lb, ub)
        sym = sf.findSymmetries(linProblem)
        self.assertEqual(sym[:6], [0, 0, 2, 3, 2, 3])

