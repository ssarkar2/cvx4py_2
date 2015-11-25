from . cvxParserGP import cvxParserGP
from . cvxParser import cvxParser
from . helpers import profile, default_locals
from . exceptions import DCPError, QCMLException
from . ast.expressions import Variable
from . ast import NodeVisitor
from . codegens import Codegen
from . codegens.python import PythonCodegen
#import ecos
import sys
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
        print self.cvxProgramString
        self.locals = locals

    def prob2socp(self):
        return self.__codegen.prob2socp

    def socp2prob(self):
        return self.__codegen.socp2prob

    def parse(self):
        print 'Parsing...'
        self.parserObj = cvxParser(self.locals)  #create a parser class and then call the parse function on it.
        self.program = self.parserObj.parse(self.cvxProgramString)
        print self.program


    def canonicalize(self):
        print 'Canonicalizing...'
        self.program.canonicalize()
        print self.program

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
        varDecl = self.parserObjGP.VarDeclaration
        objective = self.parserObjGP.Objective
        ineqConstraints = self.parserObjGP.ineqConstraints
        eqConstraints = self.parserObjGP.eqConstraints
        print ineqConstraints
        print eqConstraints
        print varDecl
        print objective

    def solveProblem(self):
        print "Starting..."
        print self.cvxProgramString

        if (self.isGPMode()):
            self.gpparse()
            self.gpCodegen();
            pass
        else:
            self.parse()
            res = self.solve(self.locals)
            self.codegen()
            self.save("problemPython")










