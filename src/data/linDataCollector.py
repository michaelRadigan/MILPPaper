import os as os
import linearProblem as lp
import pickle as pickle
from data import linData as ld
import pebble as pebble
import time as time


def constructLinProblem(problemName):
    pickledProblem = pickle.load(open("pickle/" + problemName, "rb"))
    return lp.LinearProblem(pickledProblem.Aeq.tocoo(), pickledProblem.Aineq.tocoo(), pickledProblem.beq,
                            pickledProblem.bineq, pickledProblem.f, pickledProblem.lb, pickledProblem.ub)


# instancePath = '/home/michael/4thYear/project/scripts/parsedInstances'
# problemNames = next(os.walk(instancePath))[1]

# Note that this ay have been broken by the directory move in the large refactor
def pickleProblem(problemName):
    print("Starting: " + problemName)
    linProblem = constructLinProblem(problemName)
    eqIntTime, eqIntSymmetry = linProblem.findEqSymmetriesIntermediate()
    ineqIntTime, ineqIntSymmetry = linProblem.findIneqSymmetriesIntermediate()
    eqSupTime, eqSupSymmetry = linProblem.findEqSymmetriesSuperposition()
    ineqSupTime, ineqSupSymmetry = linProblem.findIneqSymmetriesSuperposition()

    if linProblem.eqGraphSuperposition is not None:
        eqSupNumNodes = linProblem.eqGraphSuperposition.number_of_vertices
        eqSupPartition = linProblem.eqPartitionSuperposition
    else:
        eqSupNumNodes = 0
        eqSupPartition = None
    if linProblem.ineqGraphSuperposition is not None:
        ineqSupNumNodes = linProblem.ineqGraphSuperposition.number_of_vertices
        ineqSupPartition = linProblem.ineqPartitionSuperposition
    else:
        ineqSupNumNodes = 0
        ineqSupPartition = None
    if linProblem.ineqGraphIntermediate is not None:
        ineqIntNumNodes = linProblem.ineqGraphIntermediate.number_of_vertices
        ineqIntPartition = linProblem.ineqPartitionIntermediate
    else:
        ineqIntNumNodes = 0
        ineqIntPartition = None

    if linProblem.eqGraphIntermediate is not None:
        eqIntNumNodes = linProblem.eqGraphIntermediate.number_of_vertices
        eqIntPartition = linProblem.eqPartitionIntermediate
    else:
        eqIntNumNodes = 0
        eqIntPartition = None

    # problemData = ld.LinData(problemName, eqSupTime, ineqSupTime, eqSupSymmetry, ineqSupSymmetry,
    #             eqSupNumNodes, ineqSupNumNodes, eqSupPartition, ineqSupPartition,
    #             eqIntTime, ineqIntTime, eqIntSymmetry, ineqIntSymmetry,
    #             eqIntNumNodes, ineqIntNumNodes, eqIntPartition, ineqIntPartition)

    # picklePath = '/home/michael/4thYear/project/src/linData2'
    # pickle.dump(problemData, open(picklePath + '/' + problemName, "wb"))
    # return 0


def pickleIntEq(problemName):
    linProblem = constructLinProblem(problemName)
    eqIntTime, eqIntSymmetry = linProblem.findEqSymmetriesIntermediate()

    if linProblem.eqGraphIntermediate is not None:
        eqIntNumNodes = linProblem.eqGraphIntermediate.number_of_vertices
        eqIntPartition = linProblem.eqPartitionIntermediate
    else:
        eqIntNumNodes = 0
        eqIntPartition = None
    problemData = ld.LinData(problemName, True, True, eqIntTime, eqIntSymmetry,
                             eqIntNumNodes, eqIntPartition)
    picklePath = '/home/michael/4thYear/project/src/linData2/intEq'
    pickle.dump(problemData, open(picklePath + '/' + problemName, "wb"))


def pickleIntIneq(problemName):
    linProblem = constructLinProblem(problemName)
    ineqIntTime, ineqIntSymmetry = linProblem.findIneqSymmetriesIntermediate()
    if linProblem.ineqGraphIntermediate is not None:
        ineqIntNumNodes = linProblem.ineqGraphIntermediate.number_of_vertices
        ineqIntPartition = linProblem.ineqPartitionIntermediate
    else:
        ineqIntNumNodes = 0
        ineqIntPartition = None

    problemData = ld.LinData(problemName, False, True, ineqIntTime, ineqIntSymmetry,
                             ineqSupNumNodes, ineqIntPartition)

    picklePath = '/home/michael/4thYear/project/src/linData2/intIneq'
    pickle.dump(problemData, open(picklePath + '/' + problemName, "wb"))


def pickleSupEq(problemName):
    linProblem = constructLinProblem(problemName)
    print("constructed sup eq for : " + problemName)
    eqSupTime, eqSupSymmetry = linProblem.findEqSymmetriesSuperposition()
    if linProblem.eqGraphSuperposition is not None:
        eqSupNumNodes = linProblem.eqGraphSuperposition.number_of_vertices
        eqSupPartition = linProblem.eqPartitionSuperposition
    else:
        eqSupNumNodes = 0
        eqSupPartition = None
    problemData = ld.LinData(problemName, True, False, eqSupTime, eqSupSymmetry,
                             eqSupNumNodes, eqSupPartition)
    picklePath = '/home/michael/4thYear/project/src/linData2/supEq'
    pickle.dump(problemData, open(picklePath + '/' + problemName, "wb"))


def pickleSupIneq(problemName):
    linProblem = constructLinProblem(problemName)
    print("constructed sup inEq for : " + problemName)
    ineqSupTime, ineqSupSymmetry = linProblem.findIneqSymmetriesSuperposition()
    if linProblem.ineqGraphSuperposition is not None:
        ineqSupNumNodes = linProblem.ineqGraphSuperposition.number_of_vertices
        ineqSupPartition = linProblem.ineqPartitionSuperposition
    else:
        ineqSupNumNodes = 0
        ineqSupPartition = None

    problemData = ld.LinData(problemName, True, False, ineqSupTime, ineqSupSymmetry,
                             ineqSupNumNodes, ineqSupPartition)
    picklePath = '/home/michael/4thYear/project/src/linData2/supIneq'
    pickle.dump(problemData, open(picklePath + '/' + problemName, "wb"))


# notTriedYet = ['germanrr', 'bley_xl1', 'neos-933638', 'core4872-1529', 'ns2118727', 'neos15']

# [pickleProblem(x) for x in notTriedYet]


instancePath = "/home/michael/4thYear/project/src/linData2/intEq"
problemNames = next(os.walk(instancePath))[2]
# problemNames = ['enlight16.p']

with pebble.ProcessPool(max_workers=2) as pool:
    future = pool.map(pickleSupIneq, problemNames, timeout=600)

    iterator = future.result()

    while True:
        try:
            result = next(iterator)
        except StopIteration:
            break
        except TimeoutError as error:
            print("function took longer than %d seconds" % error.args[1])
        except pebble.ProcessExpired as error:
            print("%s. Exit code: %d" % (error, error.exitcode))
        except Exception as error:
            print("function raised %s" % error)
            print(error.__traceback__)  # Python's traceback of remote process

print("sleeping for 5 seconds")
time.sleep(5)
# multiple_results = [pool.schedule(pickleProblem, (problemName,), timeout=60) for problemName in notTriedYet]
#    multiple_results = [pool.schedule(pickleProblem, (problemName,), timeout=600) for problemName in problemNames]

#    for res in multiple_results:
#        try:
#            res.get()
#        except TimeoutError:
#            print("We lacked patience and got a multiprocessing.TimeoutError")
#        except MemoryError:
#            print("We lacked memory and got a multiprocessing.MemoryError")
