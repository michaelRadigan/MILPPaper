from linsym import linearProblem as lp
from scipy.sparse import coo_matrix
import numpy as np


def parse(filepath):
    with open(filepath, "r") as fo:
        return parse_lines(fo)


# TODO[michaelr]: We will unmock the parts that aren't defined as we go
def make_lp(A, obj, rhs):
    numVars = A.shape[1]
    numConstraints = A.shaoe[0]

    f = np.zeros(numVars)
    lb = np.zeros(numVars)
    ub = np.zeros(numVars)

    bineq = np.zeros(numConstraints)
    beq = np.zeros(numConstraints)

    # TODO[michaelr]: Definitely possible to just populate these directly rather
    # TODO[michaelr]: than building up tuples then iterating through the tuples
    for i, val in rhs:
        beq[i] = val

    for i, val in obj:
        f[i] = val
    for i, val in lb:
        lb[i] = val
    for i, val in ub:
        ub[i] = val

    return lp.LinearProblem(A, A, beq, bineq, f, lb, ub)


def validate_first_line(first):
    nameIdentifier, name = first.split()

    if nameIdentifier != "NAME":
        raise Exception("This is not a valid MPS file - NAME")


def validate_second_line(second):
    if second.strip() != "ROWS":
        raise Exception("This is not a valid MPS file - ROWS")


def validate_start_marker(line):
    if "'MARKER'" not in line or "'INTORG'" not in line:
        raise Exception("This is not a valid MPS file - missing marker")


def validate_rhs(line):
    if line.strip() != "RHS":
        raise Exception("This is not a valid MPS file - RHS")


def read_line(file_object):
    line = file_object.readline()
    if not line:
        raise Exception("This is not a valid MPS file - EMPTY")
    return line


def is_end_marker(line):
    return "'MARKER'" in line and "'INTEND'" in line


def read_until(fo, condition):
    while True:
        line = read_line(fo)
        if condition(line):
            break
        yield line


def parse_lines(fo):
    validate_first_line(read_line(fo))
    validate_second_line(read_line(fo))

    numRows = 0
    rows = {}
    objName = ""

    # Could even just have aa dict of rowName -> Type?
    for line in read_until(fo, lambda l: l.strip() == "COLUMNS"):
        # TODO[michaelr]: Deal with all of the row types properly
        rowType, row = line.split()
        if rowType == "E":
            rows[row] = numRows
            numRows += 1
        elif rowType == "N":
            objName = row
        else:
            raise Exception("Unknown row type: " + rowType)

    validate_start_marker(read_line(fo))

    data, col, row, obj = [], [], [], []
    columns = {}
    numColumns = 0

    for line in read_until(fo, is_end_marker):
        columnName, rowName, val = line.split()
        if not (columnName in columns):
            columns[columnName] = numColumns
            numColumns += 1
        if rowName == objName:
            obj.append((columns[columnName], val))
        elif rowName in rows:
            data.append(val)
            col.append(columns[columnName])
            row.append(rows[rowName])
        else:
            raise Exception("Unknown row: { " + rowName + "} in column: " + columnName)
    A = coo_matrix((data, (row, col)), shape=(len(rows), len(columns)))

    # TODO[michaelr]: Going to assume that "ROWS" is always required, maybe it isn't?
    validate_rhs(read_line(fo))

    rhs = []
    for line in read_until(fo, lambda l: l.strip() == "BOUNDS"):
        _, rowName, val = line.split()
        rhs.append((rows[rowName], val))

    ub = []
    lb = []
    for line in read_until(fo, lambda l: l.strip() == "ENDDATA"):
        boundType, _, columnName, val = line.split()
        if boundType == "UP":
            ub.append((columns[columnName], val))
        elif boundType == "LI":
            lb.append((columns[columnName], val))
        else:
            raise Exception("")

    return make_lp(A, obj, rhs, ub, lb)

