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

    def parse(self, cvxProgramString):
        return self.parserObj.parse(cvxProgramString)

    def p_program(self,p):
        '''program :  cvxbegin GP statements objective statements cvxend
                   |  cvxbegin GP statements objective cvxend
        '''

        print 'p_program_gp'
        #constraints = p[3]
        #if len(p) > 6: constraints.extend(p[5])
        #constr =  ProgramConstraintsGP(constraints)
        #data = ProgramDataGP(self.dimensions,self.parameters,self.variables)
        #p[0] = GP(p[4],constr,data)
        pass

    def p_program_empty(self,p):
        'program : empty'
        pass

    def p_empty(self,p):
        'empty : '
        pass

    def p_objective(self,p):
        '''objective : SENSE posy NL
                     | SENSE posy NL SUBJECT TO NL'''

        #p[0] = ProgramObjectiveGP(p[1],p[2])
        pass

    def p_cvxbegin(self, p):
        '''cvxbegin : CVX_BEGIN GP SEMICOLON
                    | CVX_BEGIN GP COMMA
                    | CVX_BEGIN GP NL
        '''
        self.mode = 1 #GP mode
        print 'in gp mode'


    def p_cvxend(self,p):
        '''cvxend : CVX_END
                  | CVX_END NL
                  | CVX_END SEMICOLON
                  | CVX_END COMMA'''
        pass


    def p_create_identifier(self,p):
        'create : VARIABLE array'
        #(name, shape) = p[2]
        #if(p[1] == 'variable'):
            #self.decl_variables[name] = Variable(name, shape)
        pass

    def p_create_identifiers(self,p):
        'create : VARIABLES arraylist'
        #if(p[1] == 'variables'):
            #self.decl_variables.update({name: Variable(name, shape) for (name,shape) in p[2]})
        pass

    def p_create_dual_variable(self, p):
        '''create : DUAL VARIABLE ID'''
        pass

    def p_create_dual_variables(self, p):
        'create : DUAL VARIABLES idlist'
        pass

    def p_array_identifier(self,p):
        'array : ID LPAREN dimlist RPAREN'
        #self._check_if_defined(p[1], p.lineno(1), p.lexpos(1))
        #p[0] = (p[1], Shape(p[3]))

    def p_array_identifier_scalar(self, p):
        '''array : ID
                 | ID LPAREN RPAREN
        '''
        self._check_if_defined(p[1], p.lineno(1), p.lexpos(1))
        p[0] = (p[1],Scalar())

    def p_arraylist_list(self,p):
        'arraylist : arraylist array'
        #p[0] = p[1] + [p[2]]

    def p_arraylist_array(self,p):
        'arraylist : array'
        #p[0] = [p[1]]

    """ def p_dimlist_list(self,p):
        '''dimlist : dimlist COMMA ID
                   | dimlist COMMA INT
        '''
    """

    def p_dimlist_singleton(self,p):
        '''dimlist : INT
                   | ID
        '''
        temp = self.locals.get(p[1], p[1])
        self._check_dimension(temp, p.lineno(1), p.lexpos(1))
        p[0] = [temp]

    def p_idlist_list(self,p):
        '''idlist : idlist ID'''
        pass

    def p_idlist_id(self,p):
        'idlist : ID'
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
                     | create
                     | chained_constraint
                     | empty
        '''
        pass

    def p_chained_constraint(self, p):
        '''chained_constraint : posy LESSTHANEQUAL mono GREATERTHANEQUAL posy
                      | mono GREATERTHANEQUAL posy LESSTHANEQUAL mono

        '''
        if p[2] == '<=' or p[2] == '<':
            p[0] = [ p[1] <= p[3], p[3] >= p[5] ]
        else:
            p[0] = [ p[1] >= p[3], p[3] <= p[5] ]


    def p_constraint(self,p):
        '''constraint : mono LOGICALEQUAL mono
                      | posy LESSTHANEQUAL mono
                      | mono GREATERTHANEQUAL posy
        '''
        if p[2] == '==':
            p[0] = [p[1] == p[3]]
        elif p[2] == '<=' or p[2] == '<':
            p[0] = [p[1] <= p[3]]
        else: # p[2] == '>=' or p[2] == '>':
            p[0] = [p[1] >= p[3]]




    def p_monomial_prod(self, p):
        '''mono : mono TIMES mono'''
        #p[0] = p[1] * p[3]
        pass

    def p_monomial_div(self, p):
        '''mono : mono DIVIDE mono'''
        pass

    def p_monomial_power(self, p):
        '''mono : mono POWER FLOAT
                | mono POWER INT'''
        pass

    def p_monomial_const(self, p):
        '''mono : ID
                | INT
                | FLOAT'''
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

    def p_error(self, t):
        print("Syntax error at '%s'" % t.value)



