from cvxLexer import cvxLexer
from ply import yacc
##from . exceptions import ParseError
##from . ast.expressions import Number, Parameter, Variable, Sum, Transpose
##from . ast.atoms import atoms
##from . ast import SOCP, ProgramData, ProgramConstraints, ProgramObjective
##from . properties.sign import Neither, Positive, Negative
##from . properties.shape import Scalar, Shape, isscalar
import numpy as np
from Monomial import *
from Posynomial import *

#var is a list of 2 elements: [varname(string), dimension/idx(int)]  #note, if var is encountered in objective, the int is its dimension, else if its in a constraint, its the index
#varlist is a list of vars


#http://cvxr.com/cvx/doc/gp.html
class cvxParserGP(object):
    # operator precedence
    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('left', 'POWER'),
    )

    def __init__(self, locals = {}):
        self.lexerObj = cvxLexer()
        self.lexerObj.buildLex()
        self.tokens = self.lexerObj.tokens
        self.parserObj = yacc.yacc(module = self)
        self.locals = locals
        self.decl_vars = {}
        self.VarDeclaration = []
        self.eqConstraints = []  #should be in canonical form mono == 1
        self.ineqConstraints = [] #should ne in canonical form posy <= 1

    def parse(self, cvxProgramString):
        return self.parserObj.parse(cvxProgramString)

    def p_program(self,p):
        '''program :  cvxbegin statements objective statements cvxend
                   |  cvxbegin statements objective cvxend
        '''

        #print 'p_program_gp'
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
                     | SENSE posy NL SUBJECT TO NL
                     | SENSE mono NL
                     | SENSE mono NL SUBJECT TO NL
        '''

        #p[0] = ProgramObjectiveGP(p[1],p[2])

        self.Objective = []

        if(p[1] == 'minimize'):                             # Objective is a list ['minimize',<Posynomial/Monomial Object>]
            self.Objective.append('Minimize')
            self.Objective.append(p[2])

        elif(p[1] == 'maximize'and isinstance(p[2],Monomial)): # or ['maximize',<Monomial object>]
            self.Objective.append('Maximize')
            self.Objective.append(p[2])

        elif(p[1] == 'find'):                               # or feasibility problem ['minimize',1]    #To do TODO: check how feasibility problems are handled
            self.Objective.append('minimize')
            p[2] = Monomial()
            self.Objective.append(p[2])
        else:
            print 'Error in objective'


        '''
        print self.Objective[0]
        if isinstance(p[2],Posynomial):
            for i in self.Objective[1].posyList:
                print i.monoDict
        else:
            print self.Objective[1].monoDict
        pass
        '''

    def p_cvxbegin(self, p):
        '''cvxbegin : CVX_BEGIN GP SEMICOLON
                    | CVX_BEGIN GP COMMA
                    | CVX_BEGIN GP NL
        '''
        self.mode = 1 #GP mode


    def p_cvxend(self,p):
        '''cvxend : CVX_END
                  | CVX_END NL
                  | CVX_END SEMICOLON
                  | CVX_END COMMA'''
        pass


    def p_create_identifier(self,p):
        'create : VARIABLE var'
        #(name, shape) = p[2]
        #if(p[1] == 'variable'):
            #self.decl_variables[name] = Variable(name, shape)
        self.addVar(p[2])
        #print p[2][0] + ' = Variable(' + str(p[2][1]) + ')'
        self.VarDeclaration.append((p[2][0], p[2][1]))
        pass

    def p_create_identifiers(self,p):
        'create : VARIABLES varlist'
        #if(p[1] == 'variables'):
            #self.decl_variables.update({name: Variable(name, shape) for (name,shape) in p[2]})
        for item in p[2]:
            self.addVar(item)
            #print item[0] + ' = Variable(' + str(item[1]) + ')'
            self.VarDeclaration.append((item[0], item[1]))
            #print(self.VarDeclaration)
        pass

    def p_create_dual_variable(self, p):
        '''create : DUAL VARIABLE ID'''
        pass

    def p_create_dual_variables(self, p):
        'create : DUAL VARIABLES idlist'
        pass

    def addVar(self, var):
        if self.decl_vars.get(var[0], None) is not None:
            print 'ERROR: adding already declared variable'
            #TODO to do: add an error-exit function
        else:
            self.decl_vars[var[0]] = var[1]


    def p_var_identifier(self,p):
        'var : ID LPAREN dimlist RPAREN'
        #self._check_if_defined(p[1], p.lineno(1), p.lexpos(1))
        #p[0] = (p[1], Shape(p[3]))
        p[0] = [p[1], p[3]]

    def p_var_identifier_scalar(self, p):
        '''var : ID
                 | ID LPAREN RPAREN
        '''
        #self._check_if_defined(p[1], p.lineno(1), p.lexpos(1))
        #p[0] = (p[1],Scalar())
        p[0] = [p[1], 1]  #var

    def p_varlist_list(self,p):
        'varlist : varlist var'
        p[0] = p[1] + [p[2]]  #append to list

    def p_varlist_var(self,p):
        'varlist : var'
        p[0] = [p[1]]

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
        p[0] = temp

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
                      | mono LOGICALEQUAL mono GREATERTHANEQUAL posy
                      | posy LESSTHANEQUAL mono LOGICALEQUAL mono
                      | mono LESSTHANEQUAL posy GREATERTHANEQUAL mono
                      | mono LESSTHANEQUAL mono GREATERTHANEQUAL mono
                      | mono LESSTHANEQUAL mono LESSTHANEQUAL mono

        '''
        if p[2] == '<=' or p[2] == '<':
            p[0] = [ p[1] <= p[3], p[3] >= p[5] ]
        else:
            p[0] = [ p[1] >= p[3], p[3] <= p[5] ]
        #TO DO
        #fill out this function


    def p_constraint(self,p):
        '''constraint : mono LOGICALEQUAL mono
                      | posy LESSTHANEQUAL mono
                      | mono GREATERTHANEQUAL posy
                      | mono LESSTHANEQUAL mono
                      | mono GREATERTHANEQUAL mono
        '''
        """
        if p[2] == '==':
            p[0] = [p[1] == p[3]]
        elif p[2] == '<=' or p[2] == '<':
            p[0] = [p[1] <= p[3]]
        else: # p[2] == '>=' or p[2] == '>':
            p[0] = [p[1] >= p[3]]
        """
        if p[2] == '==':
            tmp = p[1].mono_division_by_mono(p[3])
            self.eqConstraints.append(tmp)
        elif p[2] == '<=' or p[2] == '<':
            if isinstance(p[1], Posynomial):
                tmp = p[1].posy_division_by_mono(p[3])
                self.ineqConstraints.append(tmp)
            else:
                tmp = p[1].mono_division_by_mono(p[3])
                self.ineqConstraints.append(tmp)
        elif p[2] == '>=' or p[2] == '>':
            if isinstance(p[3], Posynomial):
                tmp = p[3].posy_division_by_mono(p[1])
                self.ineqConstraints.append(tmp)
            else:
                tmp = p[3].mono_division_by_mono(p[1])
                self.ineqConstraints.append(tmp)
        #print self.ineqConstraints
        #print self.eqConstraints

        """
        for i in self.constraints:
            if (type(i[0]) == 'Monomial'):
                print i.monoDict
            elif (type(i[0]) == 'Posynomial'):
                for j in i[0].posyList:
                    print j.monoDict
                    print '+'
            print i[1],i[2]
        """
    def p_monomial_prod(self, p):
        '''mono : mono TIMES mono'''
        p[0] = p[1].mono_times_mono(p[3])
        """
        print 'p_monomial_prod'
        print p[0].monoDict
        """

    def p_monomial_div(self, p):
        '''mono : mono DIVIDE mono'''
        p[0] = p[1].mono_division_by_mono(p[3])

    def p_monomial_power(self, p):
        '''mono : mono POWER FLOAT
                | mono POWER INT'''
        p[0] = p[1].mono_raise_to_pow(float(p[3]))

    def checkVar(self, varname, varidx):
        temp = self.decl_vars.get(varname, None)
        if temp is None:
            print 'Variable not declared',varname
            return False
        else:
            if temp < varidx:
                print 'Indexing exceeds dimension:', varname, temp, varidx
                return False
            else:
                return True

    def p_monomial_const(self, p):  #p[0] is a string (if its ID) or a number
        '''mono : var
                | INT
                | FLOAT'''
        if isinstance(p[1], float):
            p[0] = Monomial().mono_addCoeff(float(p[1]))
        elif isinstance(p[1], int):
            p[0] = Monomial().mono_addCoeff(int(p[1]))
        else:
            temp = self.locals.get(p[1][0], None)
            if temp is None:
                if self.checkVar(p[1][0], p[1][1]):
                    p[0] = Monomial().mono_multiply(1, p[1][0], float(p[1][1]))
                else:
                    print 'Error: incorrectly using variable', p[1]
            else:
                p[0] = Monomial().mono_addCoeff(temp)

        """
        print 'p_monomial_const'
        print p[0].monoDict
        """
    def p_posynomial(self, p):
        '''posy : mono PLUS mono'''
        p[0] = (Posynomial().posy_add_mono(p[1])).posy_add_mono(p[3])
        """
        print 'p_posynomial'
        for i in p[0].posyList:
            print i.monoDict
        """

    def p_posynomial_add_posynomial(self, p):
        '''posy : posy PLUS posy '''
        p[0] = p[1].posy_add_posy(p[3])
        #print 'p_posynomial_add_posynomial'
        #for i in p[0].posyList:
        #    print i.monoDict

    def p_posynomial_add_monomial(self,p):
        ''' posy : posy PLUS mono  '''
        p[0] = p[1].posy_add_mono(p[3])
        #for i in p[0].posyList:
        #    print i.monoDict


    def p_posynomial_prod(self, p):
        '''posy : posy TIMES posy'''
        p[0] = p[1].posy_times_posy(p[3])

    def p_posynomial_prod_mono(self, p):
        '''posy : posy TIMES mono
                | mono TIMES posy'''
        if isinstance(p[1], Posynomial):
            p[0] = p[1].posy_times_mono(p[3])
        else:
            p[0] = p[3].posy_times_mono(p[1])

    def p_posynomial_div(self, p):
        '''posy : posy DIVIDE mono'''
        p[0] = p[1].posy_division_by_mono(p[3])

    def p_posynomial_power(self, p):
        '''posy : posy POWER INT'''
        p[0] = p[1].posy_power(int(p[3]))

    def p_posymonial_bracket(self,p):
        '''posy : LPAREN posy RPAREN'''
        p[0] = p[2]

    def p_monomial_bracket(self,p):
        '''mono : LPAREN mono RPAREN'''
        p[0] = p[2]

    def p_error(self, t):
        print("Syntax error at '%s'" % t.value)



