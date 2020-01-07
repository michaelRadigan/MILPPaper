def parseIntMatrixFromFile( filename):
    #f = open('/home/michael/4thYear/project/scripts/cov1075Aineq.txt', 'r')
    f = open(filename, 'r')
    return [[int(num) for num in line.strip().split('\t')] for line in f]