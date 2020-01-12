# Script to translate linear problems to python
import os as os
import scipy.io as sio
#import numpy as mp
import linearProblem as lp
import pickle as pickle

instancePath = '/home/michael/4thYear/project/scripts/parsedInstanceinstancePaths'
problemNames = next(os.walk(instancePath))[1]

for problemName in problemNames:
    problemPath = instancePath + '/' + problemName

    allFiles = next(os.walk(problemPath))[2]

    allMatFiles = [x for x in allFiles if x.endswith(".mat")]

    if len(allMatFiles) != 8:
        continue

    print(problemPath + '/' + 'Aeq.mat')
    Aeq = sio.loadmat(problemPath + '/' + 'Aeq.mat')['Aeq']
    Aineq = sio.loadmat(problemPath + '/' + 'Aineq.mat')['Aineq']
    beq = sio.loadmat(problemPath + '/' + 'beq.mat')['beq']
    bineq = sio.loadmat(problemPath + '/' + 'bineq.mat')['bineq']
    f = sio.loadmat(problemPath + '/' + 'f.mat')['f']
    intcon = sio.loadmat(problemPath + '/' + 'intcon.mat')['intcon']
    lb = sio.loadmat(problemPath + '/' + 'lb.mat')['lb']
    ub = sio.loadmat(problemPath + '/' + 'ub.mat')['ub']

    problem = lp.LinearProblem(Aeq, Aineq, beq, bineq, f, intcon, lb, ub)

    picklePath = '/home/michael/4thYear/project/src/pickle/'
    pickle.dump(problem, open(picklePath + problemName + '.p', "wb"))