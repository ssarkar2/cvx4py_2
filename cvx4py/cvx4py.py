from . cvxParser import cvxParser
from . helpers import profile, default_locals
from . exceptions import DCPError, QCMLException
from . ast.expressions import Variable
from . ast import NodeVisitor
from . codegens import Codegen
from . codegens.python import PythonCodegen
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
        self.locals = locals


    def solve(self):
        print "Starting..."
        print self.cvxProgramString

        print 'Parsing...'
        self.parserObj = cvxParser(self.locals)  #create a parser class and then call the parse function on it.
        self.program = self.parserObj.parse(self.cvxProgramString)
        print self.program

        print 'Canonicalizing...'
        self.program.canonicalize()
        print self.program

        #self.__codegen = PythonCodegen()
        #self.__codegen.visit(self.program)
        #self.__codegen.codegen()  # generate the prob2socp and socp2prob functions









