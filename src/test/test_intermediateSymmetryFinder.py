from unittest import TestCase
from linearProblem import LinearProblem
import numpy as np
from scipy.sparse import csr_matrix
import intermediateSymmetryFinder as sf


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
        [1, 0, 1, 0, 0, 0],
        [1, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0],
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

    def test_simpleUnweightedMatrixOnly(self):
        Aeq = csr_matrix([np.array(x) for x in self.constraintMatrix]).tocoo()
        beq = np.array([[1], [1], [1], [1], [1], [1], [1]])


        # TODO[michaelr]: Clearly this is wrong but just making it work with what we already have...
        f = np.array([[1], [1], [1], [1], [1], [1]])
        intcon = np.array([[1], [1], [1], [1], [1], [1]])
        lb = np.array([[1], [1], [1], [1], [1], [1]])
        ub = np.array([[1], [1], [1], [1], [1], [1]])

        # TODO[michaelr]: Fx this! Passing in the eq to ineq to get around the awful design
        linProblem = LinearProblem(Aeq, Aeq, beq, beq, f, intcon, lb, ub)
        sym = sf.findSymmetries(linProblem)
        print(sym)
        self.assertEqual(sym, [0, 0, 2, 2, 2, 2, 6, 7, 7, 7, 7, 11, 11])


'''
    def testSimpleUnweightedSymmetries(self):
        s = SymmetryFinder(self.constraintMatrix)
        symmetries = s.get_symmetries()
        symmetries.sort()

        self.assertEqual(symmetries, [{0, 1}, {2, 3, 4, 5}])

    def testSimpleWeightedSymmetries(self):
        s = SymmetryFinder(self.weightedConstraintMatrix)
        symmetries = s.get_symmetries()
        symmetries.sort()
        self.assertEqual(True, False)
        self.assertEqual(symmetries, [{0, 1}, {2, 3, 4, 5}])

    def testLargerUnweightedSymmetries(self):
        s = SymmetryFinder(self.largerConstraintMatrix)
        symmetries = s.get_symmetries()
        symmetries.sort()
        self.assertEqual(symmetries, [{0, 1, 2, 3}, {4, 5, 6, 7, 8, 9, 10, 11}])

    def testLargerWeightedSymmetries(self):
        s = SymmetryFinder(self.largerWeightedConstraintMatrix)
        symmetries = s.get_symmetries()
        symmetries.sort()

        self.assertEqual(symmetries, [{0, 2}, {1, 3}, {4, 5, 8, 9}, {6, 7, 10, 11}])

    def testLargerUnweightedSymmetriesWithSimpleLinearObjectiveFunction(self):
        s = SymmetryFinder(self.largerConstraintMatrix, c=self.objectiveTest)
        symmetries = s.get_symmetries()
        symmetries.sort()

        self.assertEqual(symmetries, [{0}, {1, 3}, {2}, {4, 5}, {10, 11, 6, 7}, {8, 9}])
'''
