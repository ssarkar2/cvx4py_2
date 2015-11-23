from cvxLexer import cvxLexer
from ply import yacc
##from . exceptions import ParseError
##from . ast.expressions import Number, Parameter, Variable, Sum, Transpose
##from . ast.atoms import atoms
##from . ast import SOCP, ProgramData, ProgramConstraints, ProgramObjective
##from . properties.sign import Neither, Positive, Negative
##from . properties.shape import Scalar, Shape, isscalar
import numpy as np


#http://cvxr.com/cvx/doc/gp.html
class cvxParserGP(object):
    # operator precedence
    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
    )

    def __init__(self, locals = {}):
        self.lexerObj = cvxLexer()
        self.lexerObj.buildLex()
        self.tokens = self.lexerObj.tokens
        self.parserObj = yacc.yacc(module = self)

    def p_program(self,p):
        '''program :  cvxbegin statements cvxend
        '''
        pass

    def p_cvxbegin(self, p):
        '''cvxbegin : CVX_BEGIN
                    | cvxbegin SEMICOLON
                    | cvxbegin COMMA
                    | cvxbegin NL
        '''
        pass

    def p_cvxbegin_gpmode(self, p): #TO DO: may need to expand this function to include GP mode
        '''cvxbegin : CVX_BEGIN GP
        '''
        self.mode = 1 #GP mode
        print 'in gp mode'


    def p_cvxend(self,p):
        '''cvxend : CVX_END
                  | cvxend NL
                  | cvxend SEMICOLON
                  | cvxend COMMA'''
        pass

    def p_statements_statement(self,p):
        '''statements : statement NL
                      | statement SEMICOLON
                      | statement COMMA
        '''

    def p_statements_many_statement(self,p):
        '''statements : statements  statement NL
                      | statements  statement SEMICOLON
                      | statements  statement COMMA
                      | statements  statement SEMICOLON NL
        '''

    def p_statement(self,p):
        '''statement : constraint
        '''
        pass

    def p_constraint(self,p):
        '''constraint : mono LOGICALEQUAL mono
                      | posy LESSTHANEQUAL mono
                      | mono GREATERTHANEQUAL posy
        '''
        pass


    def p_monomial_prod(self, p):
        '''mono : mono TIMES mono'''
        pass

    def p_monomial_div(self, p):
        '''mono : mono DIVIDE mono'''
        pass

    def p_monomial_power(self, p):
        '''mono : mono POWER FLOAT
                | mono POWER INT'''
        pass

    def p_monomial(self, p):
        '''mono : ID'''
        pass

    def p_posynomial(self, p):
        '''posy : mono'''
        pass

    def p_posynomial_add(self, p):
        '''posy : mono PLUS mono'''
        pass

    def p_posynomial_prod(self, p):
        '''posy : posy TIMES posy'''
        pass

    def p_posynomial_div(self, p):
        '''posy : posy DIVIDE mono'''
        pass

    def p_posynomial_power(self, p):
        '''posy : posy POWER INT'''
        pass




