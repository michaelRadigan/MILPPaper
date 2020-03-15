from linsym import linearProblem as lp
from scipy.sparse import coo_matrix
import numpy as np


def parse(filepath):
    with open(filepath, "r") as fo:
        return parse_lines(fo)


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


def validate_first_line(first):
    if first == "":
        raise Exception("This is not a valid MPS file - EMPTY")
    nameIdentifier, name = first.split()

    if nameIdentifier != "NAME":
        raise Exception("This is not a valid MPS file - NAME")


def validate_second_line(second):
    if second.strip() != "ROWS":
        raise Exception("This is not a valid MPS file - ROWS")


def validate__start_marker(line):
    if "'MARKER'" not in line or "'INTORG'" not in line:
        raise Exception("This is not a valid MPS file - missing marker")


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

    # Could even just have rowNAme -> Type?
    for line in read_until(fo, lambda l: l.split == "COLUMNS"):
        # TODO[michaelr]: Deal with all of the row types properly
        rowType, row = line.split()
        if rowType == "E":
            rows[row] = numRows
            numRows += 1
        elif rowType == "N":
            objName = row
        else:
            raise Exception("Unknown row type: " + rowType)

    validate__start_marker(read_line(fo))

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

    return make_lp(A, obj)

