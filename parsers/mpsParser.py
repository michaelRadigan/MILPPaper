from linsym import linearProblem as lp
from scipy.sparse import coo_matrix
import numpy as np
import sys
import math

# TODO[michaelr]: Lots of elif blocks that should be switches



# TODO[michaelr]: This s fucking disgusting and should be cleaned up but for now, magic number for free row
# TODO[michaelr]: This would break a solver but is still correct from a symmetry point of view
UNBOUNDED = sys.maxsize * 2 + 12463574

def parse(filepath):
    with open(filepath, "r") as fo:
        return parse_lines(fo)


# TODO[michaelr]: We will unmock the parts that aren't defined as we go
def make_lp(Aeq, Aineq, obj, rhsEq, rhsIneq, upper, lower):
    # This is just in case one of them is empty
    #TODO[michaelr]: Can certainly clean this up max business up
    numVars = max(Aeq.shape[1], Aeq.shape[0])

    f = np.zeros(numVars)
    lb = np.zeros(numVars)
    ub = np.zeros(numVars)

    # This is just in case one of them is empty
    bineq = np.zeros(max(Aineq.shape[0], 0))
    beq = np.zeros(max(Aeq.shape[0], 0))

    # TODO[michaelr]: Definitely possible to just populate these directly rather
    # TODO[michaelr]: than building up tuples then iterating through the tuples
    for i, val in rhsEq:
        beq[i] = val
    for i, val in rhsIneq:
        bineq[i] = val
    for i, val in obj:
        f[i] = val
    for i, val in upper:
        ub[i] = val
    for i, val in lower:
        lb[i] = val

    return lp.LinearProblem(Aeq, Aineq, beq, bineq, f, lb, ub)


def validate_first_line(first):
    nameIdentifier, name = first.split()

    if nameIdentifier != "NAME":
        raise Exception("This is not a valid MPS file - NAME")


def validate_second_line(second):
    if second.strip() != "ROWS":
        raise Exception("This is not a valid MPS file - ROWS")


def read_line(file_object):
    line = file_object.readline()
    if not line:
        raise Exception("This is not a valid MPS file - EMPTY")
    # TODO[michaelr]: I don't really like this
    if line.isspace():
        return read_line(file_object)
    # TODO[michaelr]: Maybe this is a bit sad?
    if "'MARKER'" in line and ("'INTORG'" in line or "'INTEND'" in line):
        return read_line(file_object)
    # TODO[michaelr]: Implement RANGES (note that some are empty)
    if line.strip() == "RANGES":
        return read_line(file_object)
    # Ignore comments
    if line.startswith("*"):
        return read_line(file_object)
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

    numEqRows, numIneqRows = 0, 0
    # TODO[michaelr]:
    eqRows, ineqRows = {}, {}
    objName = ""
    lRows, gRows, fRows = set(), set(), set()

    for line in read_until(fo, lambda l: l.strip() == "COLUMNS"):
        # TODO[michaelr]: Deal with all of the row types properly
        split = line.split()
        # TODO[michaelr]: This is to deal with weird comments (?) in rvb-sub.mos
        rowType, row = (split[0], split[1])
        #rowType, row = line.split()
        if rowType == "E":
            eqRows[row] = numEqRows
            numEqRows += 1
        elif rowType == "L":
            ineqRows[row] = numIneqRows
            lRows.add(row)
            numIneqRows += 1
        elif rowType == "G":
            ineqRows[row] = numIneqRows
            gRows.add(row)
            numIneqRows += 1
        elif rowType == "N":
            if not objName:
                objName = row
            else:
                fRows.add(row)
                ineqRows[row] = numIneqRows
                numIneqRows += 1

        else:
            raise Exception("Unknown row type: " + rowType)

    eqData, eqCol, eqRow, obj, ineqData, ineqCol, ineqRow = [], [], [], [], [], [], []
    columns = {}
    numColumns = 0

    def process_column(columnName, rowName, val, numColumns):
        if not (columnName in columns):
            columns[columnName] = numColumns
            numColumns += 1
        if rowName == objName:
            obj.append((columns[columnName], val))
        elif rowName in eqRows:
            eqData.append(val)
            eqCol.append(columns[columnName])
            eqRow.append(eqRows[rowName])
        elif rowName in ineqRows:
            if rowName in gRows:
                val *= 1
            ineqData.append(val)
            ineqCol.append(columns[columnName])
            ineqRow.append(ineqRows[rowName])
        else:
            raise Exception("Unknown row: { " + rowName + "} in column: " + columnName)
        return numColumns

    for line in read_until(fo, lambda l: l.strip() == "RHS"):
        numSplits = len(line.split())
        if numSplits == 3:
            columnName, rowName, val = line.split()
            numColumns = process_column(columnName, rowName, val, numColumns)
        elif numSplits == 5:
            columnName, rowName1, val1, rowName2, val2 = line.split()
            numColumns = process_column(columnName, rowName1, val1, numColumns)
            numColumns = process_column(columnName, rowName2, val2, numColumns)
        else:
            raise Exception("Unable to parse column definitions from line: " + line)

    Aeq = coo_matrix((eqData, (eqRow, eqCol)), shape=(len(eqRows), len(columns)))

    # Free row tangent, wantit to be all zeros with rhs inf and a
    Aineq = coo_matrix((ineqData, (ineqRow, ineqCol)), shape=(len(ineqRows), len(columns)))

    rhsEq, rhsIneq = [], []

    def process_rhs(name, value):
        if name in eqRows:
            rhsEq.append((eqRows[name], value))
        elif name in ineqRows:
            if name in gRows:
                value *= 1
            rhsIneq.append((ineqRows[name], value))

    for line in read_until(fo, lambda l: l.strip() == "BOUNDS"):
        numSplits = len(line.split())
        if numSplits == 3:

            _, rowName, val = line.split()
            process_rhs(rowName, val)
        elif numSplits == 5:
            _, rowName1, val1, rowName2, val2 = line.split()
            process_rhs(rowName1, val1)
            process_rhs(rowName2, val2)
        else:
            raise Exception("Unable to parse RHS definitions from line: " + line)

    for fRowName in fRows:
        rhsIneq.append((ineqRows[fRowName], UNBOUNDED))

    upper = []
    lower = []
    for line in read_until(fo, lambda l: l.strip() == "ENDATA"):
        # TODO[michaelr]: Do we need to cover "Made Integer" from the docs?
        numSplits = len(line.split())
        if numSplits == 4:
            boundType, _, columnName, val = line.split()
            if boundType == "UP":
                upper.append((columns[columnName], val))
            elif boundType == "LI":
                lower.append((columns[columnName], val)) #math.ceil(val)))
            elif boundType == "FX":
                lower.append((columns[columnName], val))
                upper.append((columns[columnName], val))
            elif boundType == "LO":
                lower.append((columns[columnName], val)) #math.ceil(val)))
            elif boundType == "UP":
                lower.append((columns[columnName], val))
            elif boundType == "UI":
                upper.append((columns[columnName], val)) #math.floor(val)))
            elif boundType == "FR":
                upper.append((columns[columnName], sys.maxsize))
                lower.append((columns[columnName], -sys.maxsize - 1))
            elif boundType == "BV":
                lower.append((columns[columnName], 0))
                upper.append((columns[columnName], 1))
            else:
                raise Exception("Unknown boundType: " + boundType + " in line: " + line)
        elif numSplits == 3:
            boundType, _, columnName = line.split()
            if boundType == "FR":
                upper.append((columns[columnName], sys.maxsize))
                lower.append((columns[columnName], -sys.maxsize - 1))
            elif boundType == "MI":
                lower.append((columns[columnName], -sys.maxsize - 1))
            elif boundType == "PL":
                upper.append((columns[columnName], sys.maxsize))
            elif boundType == "BV":
                lower.append((columns[columnName], 0))
                upper.append((columns[columnName], 1))
            else:
                raise Exception("Unknown boundType: " + boundType + "i n line " + line)
        else:
            raise Exception("Could not parse bounds from the following line: " + line)

    return make_lp(Aeq, Aineq, obj, rhsEq, rhsIneq, upper, lower)

