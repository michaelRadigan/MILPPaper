import pickle as pickle
import os as os
from decimal import Decimal
dataDir = '/home/michael/4thYear/project/src/linData2'

intEqDir = dataDir + '/intEq'
intIneqDir = dataDir + '/intIneq'
supEqDir = dataDir + '/supEq'
supIneqDir = dataDir + '/supIneq'

allIntEqDataFiles = [x for x in next(os.walk(intEqDir))[2] if x.endswith(".p")]
intEqData = [pickle.load(open(intEqDir + '/' + name, "rb")) for name in allIntEqDataFiles]

allIntIneqDataFiles = [x for x in next(os.walk(intIneqDir))[2] if x.endswith(".p")]
intIneqData = [pickle.load(open(intIneqDir + '/' + name, "rb")) for name in allIntIneqDataFiles]

allSupEqDataFiles = [x for x in next(os.walk(supEqDir))[2] if x.endswith(".p")]
supEqData = [pickle.load(open(supEqDir + '/' + name, "rb")) for name in allSupEqDataFiles]

allSupIneqDataFiles = [x for x in next(os.walk(supIneqDir))[2] if x.endswith(".p")]
supInEqData = [pickle.load(open(supIneqDir + '/' + name, "rb")) for name in allSupIneqDataFiles]

eqDict = {}
# intTime, supTime,  intSymmetry, supSymmetry,intNumNodes, supNumNodes, intPartition supPartition

for intEqDatum in intEqData:
    eqDict[intEqDatum.problemName] = (intEqDatum.time, 600, intEqDatum.symmetry, [], intEqDatum.numNodes, -1, [], [] )

for supEqDatum in supEqData:
    (a, b, c, d, e, f, g, h) = eqDict[supEqDatum.problemName]
    eqDict[supEqDatum.problemName] = (a, supEqDatum.time, c, supEqDatum.symmetry, e,  supEqDatum.numNodes, [], [])

count = 0
symCount = 0
for k, v in eqDict.items():
    count += 1
    intTime, supTime, intSymmetry, supSymmetry, intNumNodes, supNumNodes, intPartition, supPartition = v
    if intTime == 0:
        continue
    if supNumNodes == -1:
        supNumNodes = '-'
    l = [str(k).replace('_', '-'), str(intNumNodes), str(supNumNodes), str('%.2f' % intTime), str('%.2f' % supTime)]
    if intSymmetry != list(range(len(intSymmetry))):
        print(intSymmetry)
    #    symCount += 1
    #print(" & ".join(map(str, l)) + " \\\\")
    #print("\\hline")

#print(count)
#print(symCount)