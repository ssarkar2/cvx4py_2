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

    def __init__(self, monoDict = {}, coeff = 1):
        self.monoDict = monoDict
        self.coeff = coeff

    def __repr__(self):
        return str(self.monoDict)

    def mono_addCoeff(self, c = 1):
        if c > 0:
            return Monomial(self.monoDict, c)
        else:
            print "Error:Coefficient of monomial is always positive!!!!"

    def mono_addterm(self,p,var_id,ind=1):
        self.monoDict[(var_id,ind)]=p
        return Monomial(self.monoDict, self.coeff)


    def mono_division(self,p,var_id,ind=1):
        if (var_id,ind) in self.monoDict:
            self.monoDict[(var_id,ind)] = self.monoDict[(var_id,ind)] - p
        else:
            self.monoDict[(var_id,ind)] = -1*p
        return Monomial(self.monoDict, self.coeff)

    def mono_division_by_mono(self,mono2):
        for (i,j) in mono2.monoDict:
            self.mono_division(mono2.monoDict[(i,j)],i,j)
        self.coeff = self.coeff/mono2.coeff
        return Monomial(self.monoDict, self.coeff)

    def mono_multiply(self,p,var_id,ind=1):
        if (var_id,ind) in self.monoDict:
            self.monoDict[(var_id,ind)] = self.monoDict[(var_id,ind)] + p
        else:
            self.monoDict[(var_id,ind)] = p
        return Monomial(self.monoDict, self.coeff)

    def mono_times_mono(self,mono2):
        for (i,j) in mono2.monoDict:
            self.mono_multiply(mono2.monoDict[(i,j)],i,j)
        self.coeff = self.coeff*mono2.coeff
        return Monomial(self.monoDict, self.coeff)

    def mono_raise_to_pow(self,p):
        for (i,j) in self.monoDict:
            self.monoDict[(i,j)] = self.monoDict[(i,j)]*p
        self.coeff = pow(self.coeff,p)
        return Monomial(self.monoDict, self.coeff)

'''
M = Monomial()
m1 = M.mono_addterm(-1,'x',1)
print m1
'''

""" M = Monomial()
M.mono_addterm(-1,'x',1)
M.mono_addterm(0,'y')
M.mono_addCoeff(2)

M2 = Monomial()
M2.mono_addCoeff(5)
M2.mono_addterm(5,'y',2)

M.mono_times_mono(M2)

print M.monoDict
print M2.monoDict
M2.mono_division_by_mono(M)
print M2.monoDict

M.mono_raise_to_pow(2)
print M.monoDict
"""