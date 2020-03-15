from linsym import linearProblem as lp
from scipy.sparse import coo_matrix
import numpy as np


# TODO[michaelr]: We should use a generator fo the lines rather than indexing in weirdly all ove the place

def parse(filePath):
    fo = open(filePath, "r")
    lines = fo.readlines()
    fo.close()
    return parse_lines(lines)


# TODO[michaelr]: We will unmock the parts that aren't defined as we go
def make_lp(A, obj):
    bineq = np.array(A.shape[1])
    beq = np.array([1 for _ in range(A.shape[0])])

    numVars = A.shape[1]

    f = np.zeros(numVars)
    for i, val in obj:
        f[i] = val

    lb = np.array([1 for _ in range(A.shape[1])])
    ub = np.array([1 for _ in range(A.shape[1])])

    return lp.LinearProblem(A, A, beq, bineq, f, lb, ub)


# Intentionally doing this absolutely filthy for no just to get it done
def parse_lines(lines):
    if len(lines) <= 0:
        raise Exception("This is not a valid MPS file - EMPTY")

    nameLine = lines[0]
    nameIdentifier, name = nameLine.split()

    if nameIdentifier != "NAME":
        raise Exception("This is not a valid MPS file - NAME")

    # For now I'm not going to pay attention to the first identifier

    rowIdentifier = lines[1]
    if rowIdentifier.strip() != "ROWS":
        raise Exception("This is nit a valid MPS file - ROWS")

    base = 2
    c = 0
    rows = {}
    objName = ""

    while lines[c + base].strip() != "COLUMNS":
        # TODO[michaelr]: Deal with all of the row types properly
        rowType, row = lines[c + base].split()
        if rowType == "E":
            rows[row] = c
            c += 1
        elif rowType == "N":
            objName = row
            base += 1
        else:
            raise Exception("Unknown row type: " + rowType)

    # TODO[michaelr]: Do this properly
    # Just a filthy way to get around MARK0000 MARKER INTORG for now
    c += base + 2
    numColumns = 0

    data, col, row = [], [], []

    obj = []

    columns = {}

    while "MARK000" not in lines[c]:
        columnName, rowName, val = lines[c].split()
        if not (columnName in columns):
            columns[columnName] = numColumns
            numColumns += 1

        if rowName == objName:
            obj.append((columns[columnName], val))
        elif rowName in rows:
            data.append(val)
            # TODO[michaelr]: Just assuming that this is the correct way round for now :)
            col.append(columns[columnName])
            row.append(rows[rowName])
        else:
            raise Exception("Unknown row: { " + rowName + "} in column: " + columnName)

        c += 1

    A = coo_matrix((data, (row, col)), shape=(len(rows), len(columns)))
    return make_lp(A, obj)
