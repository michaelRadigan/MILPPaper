from linsym import linearProblem as lp
from scipy.sparse import coo_matrix


def parse(filePath):
    fo = open(filePath, "r")
    lines = fo.readlines()
    fo.close()
    return parse_lines(lines)


# Intentionally doing this absolutely filthy for no just to get it done
def parse_lines(lines):
    if len(lines) == 0:
        raise Exception("This is not a valid MPS file - EMPTY")

    # First thing to do is to parse the name

    nameLine = lines[0]
    nameIdentifier, name = nameLine.split()

    if nameIdentifier != "NAME":
        raise Exception("This is not a valid MPS file - NAME")

    # For now I'm not going to pay attention to the first identifier

    # TODO[michaelr]: Length check again

    rowIdentifier = lines[1]
    if rowIdentifier.strip() != "ROWS":
        raise Exception("This is nit a valid MPS file - ROWS")

    base = 2
    c = 0
    rows = {}
    objName = ""

    while lines[c + base].strip() != "COLUMNS":
        # TODO[michaelr]: For now, assuming that we only have equality contraints
        # TODO[michaelr]: N will be the objective function (which we throw away for now)
        rowType, row = lines[c + base].split()
        if rowType == "E":
            rows[row] = c
            c += 1
        elif rowType == "N":
            objName = row
            base += 1
        else:
            raise Exception("Unknown row type: " + rowType)
        # TODO[michaelr]: obj here is giving us an off by one error :(


    # Just a filthy way to get around MARK0000 MARKER INTORG for now
    c += base + 3
    print("firs col: " +  lines[c])

    numColumns = 0

    data, col, row = [], [], []

    obj= []

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
            raise Exception("Unknown row: { "+ rowName + "} in column: " + columnName)

        c += 1

    A = coo_matrix((data, (row, col)), shape=(len(rows), len(columns)))
    return A