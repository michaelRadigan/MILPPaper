import pickle as pickle
import os as os
from collections import defaultdict
import matplotlib.pyplot as plt

dataDir = '/home/michael/4thYear/project/src/linData'
allDataFiles = [x for x in next(os.walk(dataDir))[2] if x.endswith(".p")]
unpickledData = [pickle.load(open(dataDir + '/' + name, "rb")) for name in allDataFiles]
allEqTimes = [x.eqTime for x in unpickledData]
allEqNumNodes = [x.eqNumNodes for x in unpickledData]

eqPartitions = []

for i in range(len(unpickledData)):
    unpickledDatum = unpickledData[i]
    if unpickledDatum.eqSymmetry is not None:
        eqPartition = defaultdict(set)
        for j, x in enumerate(unpickledDatum.eqSymmetry):
            # print(i)
            eqPartition[x].add(j)
        eqPartitions.append((i, eqPartition))

maxEqPartitionByIndex = [(i, len(max(partition.values(), key=len))) for (i, partition) in eqPartitions]

maxEqPartitionNotNull = [x[1] for x in maxEqPartitionByIndex]
matchingTimeforMaxPartition = [allEqTimes[i[0]] for i in maxEqPartitionByIndex]
matchingNumNodesForPartition = [allEqNumNodes[i[0]] for i in maxEqPartitionByIndex]

matchingMaxPartitionByNumNodes = [m / n for m, n in zip(maxEqPartitionNotNull, matchingNumNodesForPartition)]

plt.scatter(maxEqPartitionNotNull, matchingTimeforMaxPartition)
plt.show()
plt.scatter(maxEqPartitionNotNull, matchingNumNodesForPartition)
plt.show()
plt.scatter(matchingMaxPartitionByNumNodes, matchingTimeforMaxPartition)
plt.show()






