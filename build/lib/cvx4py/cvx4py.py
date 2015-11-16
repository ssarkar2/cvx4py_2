from cvxParser import cvxParser
class cvx4py(object):
    def __init__(self, cvxProgram, readFromFile, locals):
        if readFromFile == 0:
            self.cvxProgramString = cvxProgram
        else:
            with open(cvxProgram, 'r') as cvxProg:
                self.cvxProgramString = cvxProg.read()
        # always append a newline to the end
        self.cvxProgramString = self.cvxProgramString.split('\n')
        self.cvxProgramString = '\n'.join(line.strip() for line in self.cvxProgramString)
        self.cvxProgramString += '\n'
        self.locals = locals



    def parse(self):
        self.parserObj = cvxParser()  #create a parser class and hen call the aprse function on it.
        x = self.parserObj.parse(self.cvxProgramString)
        print x

    def solve(self):
        print "solving..."
        print self.cvxProgramString
        self.program = self.parse()





