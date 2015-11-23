#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      arthita
#
# Created:     23/11/2015
# Copyright:   (c) arthita 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class Monomial(object):

    def __init__(self):
        self.MonoDict = {}
        self.coeff = 1

    def Mono_addCoeff(self,c):
        if c > 0:
            self.coeff = c
        else:
            print "Error:Coefficient of monomial is always positive!!!!"

    def Mono_addterm(self,var_id,ind,p):

            self.MonoDict[(var_id,ind)]=p


    def Mono_division(self,var_id,ind,p):
            if (var_id,ind) in self.MonoDict:
                self.MonoDict[(var_id,ind)] = self.MonoDict[(var_id,ind)] - p
            else:
                self.MonoDict[(var_id,ind)] = -1*p

    def Mono_division_by_Mono(self,mono2):
            for (i,j) in mono2.MonoDict:
                self.Mono_division(i,j,mono2.MonoDict[(i,j)])
            self.coeff = self.coeff/mono2.coeff

    def Mono_multiply(self,var_id,ind,p):
        if (var_id,ind) in self.MonoDict:
            self.MonoDict[(var_id,ind)] = self.MonoDict[(var_id,ind)] + p
        else:
            self.MonoDict[(var_id,ind)] = p

    def Mono_times_mono(self,mono2):
        for (i,j) in mono2.MonoDict:
                self.Mono_multiply(i,j,mono2.MonoDict[(i,j)])
        self.coeff = self.coeff*mono2.coeff




""" M = Monomial()
M.Mono_addterm('x',1,-1)
M.Mono_addterm('y',1,0)
M.Mono_addCoeff(2)

M2 = Monomial()
M2.Mono_addCoeff(5)
M2.Mono_addterm('y',2,5)

M.Mono_times_mono(M2)

print M.MonoDict
"""