from . cvxParserGP import cvxParserGP
from . cvxParser import cvxParser
from . helpers import profile, default_locals
from . exceptions import DCPError, QCMLException
from . ast.expressions import Variable
from . ast import NodeVisitor
from . codegens import Codegen
from . codegens.python import PythonCodegen
import ecos
import sys
from Monomial import *
from Posynomial import *
import os
class cvx4py(object):
    def __init__(self, cvxProgram, readFromFile, locals = {}):
        if readFromFile == 0:
            self.cvxProgramString = cvxProgram
        else:
            with open(cvxProgram, 'r') as cvxProg:
                self.cvxProgramString = cvxProg.read()
        # always append a newline to the end
        self.cvxProgramString = self.cvxProgramString.strip().split('\n')
        self.cvxProgramString = '\n'.join(line.strip() for line in self.cvxProgramString)
        self.cvxProgramString += '\n'
        #print self.cvxProgramString
        self.locals = locals

    def prob2socp(self):
        return self.__codegen.prob2socp

    def socp2prob(self):
        return self.__codegen.socp2prob

    def parse(self):
        print 'Parsing...'
        self.parserObj = cvxParser(self.locals)  #create a parser class and then call the parse function on it.
        self.program = self.parserObj.parse(self.cvxProgramString)
        #print self.program


    def canonicalize(self):
        print 'Canonicalizing...'
        self.program.canonicalize()
        #print self.program

    def solver(self, params, dims):
        temp = self.prob2socp()
        data = temp(params, dims)
        sol = ecos.solve(**data)
        temp1 = self.socp2prob()
        result = temp1(sol['x'], sol['y'], sol['z'], dims)
        result['info'] = sol['info']

        # set the objective value
        multiplier = self.__codegen.objective_multiplier
        offset = self.__codegen.objective_offset
        if isinstance(offset, str):
            # in this case, offset is likely python *code*
            offset = eval(offset)
        result['objval'] = multiplier * sol['info']['pcost'] + offset
        return result


    def solve(self, params, local_dims = None):
        self.canonicalize()
        self.codegen()
        return self.solver(params, local_dims)

    def codegen(self):
        self.__codegen = PythonCodegen()
        self.__codegen.visit(self.program)
        self.__codegen.codegen()  # generate the prob2socp and socp2prob functions

    def save(self, name = "problem"):
        self.__codegen.save(name)

    def isGPMode(self):
        return 'gp' in self.cvxProgramString.strip().split('\n')[0]

    def gpparse(self):
        print 'Parsing GP...'
        self.parserObjGP = cvxParserGP(self.locals)  #create a parser class and then call the parse function on it.
        self.program = self.parserObjGP.parse(self.cvxProgramString)
        #print self.program


    def gpCodegen(self):
        self.program = ['import numpy as np\nfrom cvxpy import *\n']
        varDecl = self.parserObjGP.VarDeclaration
        objective = self.parserObjGP.Objective
        ineqConstraints = self.parserObjGP.ineqConstraints
        eqConstraints = self.parserObjGP.eqConstraints
        numVars = sum([itr[1] for itr in varDecl])

        #generate a mapping from current variables to an index number
        self.origToNew = {}; self.newToOrig = {}
        count = 0;
        for itr in varDecl:
            for x in range(itr[1]):
                self.origToNew[(itr[0], x+1)] = count
                self.newToOrig[count] = (itr[0], x+1)
                count = count + 1

        #generate variable declaration
        self.program = self.program + ['x = Variable(' + str(numVars) + ')']

        #generate objective string
        if isinstance(objective[1], Monomial):
            self.program = self.program + ['objective = ' + objective[0] + '(' + objective[1].log_of_mono(self.origToNew) + ')']
        else:
            # todo to do: this part is untested
            tmpp = objective[1].log_sum_exp_form(self.origToNew, self.newToOrig)
            self.program = self.program + [tmpp[0] + '\n' + tmpp[1] + '\n' + 'objective = ' + objective[0] + '(' + 'log_sum_exp(a*x+b))']
        self.program = self.program + ['constraints = [' +','.join([' x[' +str(i)+'] >= -100' for i in range(numVars)]) + ']']   #positivity constraint

        #generate equality constraints
        self.program = self.program + ['constraints = constraints + [' + itr.log_of_mono(self.origToNew) + '== 0]' for itr in eqConstraints]

        #generate inequality constraints
        for itr in ineqConstraints:
            if isinstance(itr, Monomial):
                self.program = self.program + ['constraints = constraints + [' + itr.log_of_mono(self.origToNew) + '<= 0]']
            else:
                tmpp = itr.log_sum_exp_form(self.origToNew, self.newToOrig)
                self.program = self.program + [tmpp[0] + '\n' + tmpp[1] + '\nconstraints = constraints + [log_sum_exp(a*x+b) <= 0]']

        #generale solve string
        self.program = self.program + ['prob = Problem(objective, constraints)']
        self.program = self.program + ['prob.solve()']
        #self.program = self.program + ['print x.value']

        #get objective value    #todo to do : actually get the objective value
        self.program = self.program + ['objval = ' + objective[1].get_value_string(self.origToNew)]


        #code to output solution to a text file
        self.program = self.program + ['f = open(\'soln.txt\',\'w\')\nfor i in x.value:\n    f.write(str(np.exp(i.item(0))) + \' \')\nf.write(str(objval))\nf.close()\n']

        self.programString = '\n'.join(self.program)
        self.dumpToFile("cvxpy_code.py")
        print self.programString


    def dumpToFile(self, filename):
        cvxpyFile = open(filename, "w")
        cvxpyFile.write(self.programString)
        cvxpyFile.close()


    def getAnswer(self):
        os.system('python cvxpy_code.py')
        f = open('soln.txt','r')
        soln = [float(i) for i in f.read().split()]
        self.solnDict = {}
        for i in range(len(soln)-1):
            origVar = self.newToOrig[i]
            t = self.solnDict.get(origVar[0], None)
            if t is None:
                self.solnDict[origVar[0]] = soln[i]
            else:
                if isinstance(t, float):
                    self.solnDict[origVar[0]] = [self.solnDict[origVar[0]], soln[i]]
                else:
                    self.solnDict[origVar[0]].append(soln[i])
        self.solnDict['objval'] = soln[-1] #the first numbers on the file are values of the variables, the last number is the objective value
        f.close()
        if os.name == 'nt':
            os.system('del cvxpy_code.py')
            os.system('del soln.txt')
        else:
            os.system('rm cvxpy_code.py')
            os.system('rm soln.txt')

    def isSDPMode(self):
        return 'sdp' in self.cvxProgramString.strip().split('\n')[0]

    def sdpparse(self):
        print 'Parsing SDP...'

    def solveProblem(self):
        print "Starting..."
        #print self.cvxProgramString

        if self.isGPMode():
            self.gpparse()
            self.gpCodegen()
            self.getAnswer()
        elif self.isSDPMode():
            self.sdpparse()
            self.solnDict = {}
        else:
            self.parse()
            self.solnDict = self.solve(self.locals)
            #self.codegen()
            #self.save("problemPython")
        return self.solnDict










