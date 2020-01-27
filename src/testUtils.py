# testUtils.py

import numpy as np
import random as rand
from linearProblem import LinearProblem
from scipy.sparse import csr_matrix

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

    # TODO[michaelr]: Fx this! We are currently passing in eq to ineq to get around the awful design
    return LinearProblem(A, A, beq, bineq, f, lb, ub)


def constructIneqMatrixOnlyLinProblem(A):
    beq = randArray(A.shape[1])
    bineq = np.array([1 for _ in range(A.shape[0])])

    # TODO[michaelr]: Clearly this is wrong but just making it work with what we already have...
    f = np.array([1 for _ in range(A.shape[1])])
    lb = np.array([1 for _ in range(A.shape[1])])
    ub = np.array([1 for _ in range(A.shape[1])])

    Aeq = randMatrix(A.shape[1], A.shape[0])

    # TODO[michaelr]: Fx this! We are currently passing in eq to ineq to get around the awful design
    return LinearProblem(Aeq, A, beq, bineq, f, lb, ub)


def listToSparseMatrix(matrix):
    return csr_matrix([np.array(x) for x in matrix]).tocoo()


def randMatrix(n, m):
    gen = rand.Random()
    matrix = [[gen.randint(0, 256) for _ in range(n)] for _ in range(m)]
    return listToSparseMatrix(matrix)
