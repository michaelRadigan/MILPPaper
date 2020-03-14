class LinearProblem(object):
    def __init__(self, Aeq, Aineq, beq, bineq, f, lb, ub):
        self.Aeq = Aeq.tocoo()
        self.Aineq = Aineq.tocoo()
        self.beq = beq
        self.bineq = bineq
        self.f = f
        self.lb = lb
        self.ub = ub
        self.numVarsEq = Aeq.shape[1]
        self.numVarsIneq = Aeq.shape[1]
        self.numVars = self.numVarsEq + self.numVarsIneq
        self.numConstraintsEq = Aeq.shape[0]
        self.numConstraintsIneq = Aeq.shape[0]
        self.numConstraints = self.numConstraintsEq + self.numConstraintsIneq