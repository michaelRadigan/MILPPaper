from unittest import TestCase
from symmetryFinder import *


class TestSymmetryFinder(TestCase):
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

    def testNormaliseASimple(self):
        s = SymmetryFinder(self.constraintMatrix)

        A = [[1.0, 2.0, 3.0], [2.0, 4.0, 6.0], [1.0, 2.0, 3.0]]
        b = [1, 2, 0]

        zeros, A = s.normaliseA(A, b)
        self.assertEqual(zeros, set([2]))
        self.assertEqual(A, [[1.0, 2.0, 3.0], [1.0, 2.0, 3.0], [1.0, 2.0, 3.0]])

    def testSimpleChangeOfB(self):
        b = [1, 1, 1, 1, 1, 2]
        s = SymmetryFinder(self.constraintMatrix, b=b)
        constraints = [
            [1, 1, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0],
            [1, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 1],
            [0, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 1, 1],
        ]
        self.assertEqual(constraints, self.constraintMatrix)
        symmetries = s.get_symmetries()
        # TODO: Finish test

    def testSimpleChangeOfBWithSymmetry(self):
        adjustedConstraintMatrix = [
            [1, 1, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0],
            [1, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 1],
            [0, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 2, 2],
        ]
        b = [1, 1, 1, 1, 1, 1, 2]

        s = SymmetryFinder(self.constraintMatrix)
        adjustedS = SymmetryFinder(adjustedConstraintMatrix, b=b)

        symmetries = s.get_symmetries()
        adjustedSymmetries = adjustedS.get_symmetries()

        self.assertEqual(symmetries, adjustedSymmetries)

    def testEquivalentQPartition(self):
        Q1 = [
            [1, 2, 7, 5],
            [8, 0, 9, 6],
            [100, 1, 1, 8],
            [9, 100, 6, 100]
        ]

        s = SymmetryFinder(self.constraintMatrix)
        distincts1 = s.equivalentQPartition(range(len(Q1)), Q1)
        self.assertEqual(distincts1, {0: {0, 2}, 1: {1}, 3: {3}})

    def testEquivalentQPartitionWithMultipleSymmetries(self):
        Q2 = [
            [1, 6, 5, 8],
            [4, 1, 7, 9],
            [5, 3, 1, 10],
            [2, 1, 0, 100]
        ]
        s = SymmetryFinder(self.constraintMatrix)
        distincts = s.equivalentQPartition(range(len(Q2)), Q2)
