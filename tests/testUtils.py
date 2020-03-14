# testUtils.py

import numpy as np
import random as rand
from scipy.sparse import csr_matrix

import linsym
from linsym import linearProblem

constraintMatrix = \
    [
        [1, 1, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0],
        [1, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 1],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 1],
    ]

weightedConstraintMatrix = \
    [
        [1, 1, 0, 0, 0, 0],
        [1, 0, 3, 0, 0, 0],
        [1, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 3, 0],
        [0, 1, 0, 0, 0, 1],
        [0, 0, 2, 2, 0, 0],
        [0, 0, 0, 0, 2, 2],
    ]

largerConstraintMatrix = \
    [
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

largerWeightedConstraintMatrix = \
    [
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


def randArray(n):
    gen = rand.Random()
    return np.array([gen.randint(0, 256) for _ in range(n)])


def constructEqMatrixOnlyLinProblem(A):
    bineq = randArray(A.shape[1])
    beq = np.array([1 for _ in range(A.shape[0])])

    f = np.array([1 for _ in range(A.shape[1])])
    lb = np.array([1 for _ in range(A.shape[1])])
    ub = np.array([1 for _ in range(A.shape[1])])

    Aineq = randMatrix(A.shape[1], A.shape[0])

    return linearProblem.LinearProblem(A, Aineq, beq, bineq, f, lb, ub)


def constructIneqMatrixOnlyLinProblem(A):
    beq = randArray(A.shape[0])
    bineq = np.array([1 for _ in range(A.shape[0])])

    f = np.array([1 for _ in range(A.shape[1])])
    lb = np.array([1 for _ in range(A.shape[1])])
    ub = np.array([1 for _ in range(A.shape[1])])

    Aeq = randMatrix(A.shape[1], A.shape[0])

    return linsym.linearProblem.LinearProblem(Aeq, A, beq, bineq, f, lb, ub)


def constructDoubledMatrixOnlyLinProblem(A):
    beq = np.ones(A.shape[0])
    bineq = np.ones(A.shape[0])

    f = np.ones(A.shape[1])
    lb = np.ones(A.shape[1])
    ub = np.ones(A.shape[1])

    return linsym.linearProblem.LinearProblem(A, A, beq, bineq, f, lb, ub)


def listToSparseMatrix(matrix):
    return csr_matrix([np.array(x) for x in matrix]).tocoo()


def randMatrix(n, m):
    gen = rand.Random()
    matrix = [[gen.randint(0, 256) for _ in range(n)] for _ in range(m)]
    return listToSparseMatrix(matrix)
