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

    def mono_addCoeff(self,c):
        if c > 0:
            self.coeff = c
        else:
            print "Error:Coefficient of monomial is always positive!!!!"

    def mono_addterm(self,p,var_id,ind=1):

            self.MonoDict[(var_id,ind)]=p


    def mono_division(self,p,var_id,ind=1):
            if (var_id,ind) in self.MonoDict:
                self.MonoDict[(var_id,ind)] = self.MonoDict[(var_id,ind)] - p
            else:
                self.MonoDict[(var_id,ind)] = -1*p

    def mono_division_by_mono(self,mono2):
            for (i,j) in mono2.MonoDict:
                self.mono_division(mono2.MonoDict[(i,j)],i,j)
            self.coeff = self.coeff/mono2.coeff

    def mono_multiply(self,p,var_id,ind=1):
        if (var_id,ind) in self.MonoDict:
            self.MonoDict[(var_id,ind)] = self.MonoDict[(var_id,ind)] + p
        else:
            self.MonoDict[(var_id,ind)] = p

    def mono_times_mono(self,mono2):
        for (i,j) in mono2.MonoDict:
                self.mono_multiply(mono2.MonoDict[(i,j)],i,j)
        self.coeff = self.coeff*mono2.coeff

    def mono_raise_to_pow(self,p):
        for (i,j) in self.MonoDict:
            self.MonoDict[(i,j)] = self.MonoDict[(i,j)]*p
        self.coeff = pow(self.coeff,p)


""" M = Monomial()
M.mono_addterm(-1,'x',1)
M.mono_addterm(0,'y')
M.mono_addCoeff(2)

M2 = Monomial()
M2.mono_addCoeff(5)
M2.mono_addterm(5,'y',2)

M.mono_times_mono(M2)

print M.MonoDict
print M2.MonoDict
M2.mono_division_by_mono(M)
print M2.MonoDict

M.mono_raise_to_pow(2)
print M.MonoDict
"""