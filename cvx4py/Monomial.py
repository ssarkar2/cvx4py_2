import copy
import math

class Monomial(object):

    def __init__(self, m = None, c = None):
        self.monoDict = m if m is not None else {}
        self.coeff = c if c is not None else 1


    def __str__ (self):
        return str(self.coeff) + ' ' +str(self.monoDict)

    def mono_addCoeff(self, c = 1):
        if c > 0:
            return Monomial(self.monoDict, c)
        else:
            print "Error:Coefficient of monomial is always positive!!!!"

    '''
    def mono_addterm(self,p,var_id,ind=1):  #is it needed? can't mono_multiply take care of this?
        self.monoDict[(var_id,ind)]=p
        return Monomial(self.monoDict, self.coeff)
    '''


    def mono_division(self,p,var_id,ind=1):
        monoDict = copy.deepcopy(self.monoDict)
        if (var_id,ind) in monoDict:
            monoDict[(var_id,ind)] = monoDict[(var_id,ind)] - p
        else:
            monoDict[(var_id,ind)] = -1*p
        return Monomial(monoDict, self.coeff)

    def mono_division_by_mono(self,mono2):
        div = Monomial(self.monoDict)
        for (i,j) in mono2.monoDict:
            div = div.mono_division(mono2.monoDict[(i,j)],i,j)
        return Monomial(div.monoDict, float(self.coeff)/float(mono2.coeff))


    def mono_multiply(self,p,var_id,ind=1):
        monoDict = copy.deepcopy(self.monoDict)
        if (var_id,ind) in monoDict:
            if monoDict[(var_id,ind)] + p == 0:  #the term is calcelled by the multiplication, so removing it
                monoDict.pop((var_id,ind))
            else:
                monoDict[(var_id,ind)] = monoDict[(var_id,ind)] + p
        else:
            monoDict[(var_id,ind)] = p
        return Monomial(monoDict, self.coeff)

    def mono_times_mono(self,mono2):
        prod = Monomial(self.monoDict)
        for (i,j) in mono2.monoDict:
            prod = prod.mono_multiply(mono2.monoDict[(i,j)],i,j)
        return Monomial(prod.monoDict, self.coeff*mono2.coeff)

    def mono_raise_to_pow(self,p):
        monoDict = copy.deepcopy(self.monoDict)
        for (i,j) in monoDict:
            monoDict[(i,j)] = monoDict[(i,j)]*p
        return Monomial(monoDict, pow(self.coeff,p))

    def log_of_mono(self, newVar):
        c_p = math.log(self.coeff)
        seq = []
        seq.append(str(c_p) + ' ')
        for i in self.monoDict:
            s_temp = '('+ str(self.monoDict[i]) + ')*' + 'x[' + str(newVar[i]) + '] '
            seq.append(s_temp)
        return '+ '.join(seq)

    def get_array_string(self, origToNew, newToOrig):
        string = '['
        for i in newToOrig:
            tmp = self.monoDict.get(newToOrig[i], None)
            if tmp is None:
                string = string + '0,'
            else:
                string = string + str(tmp) +','
        return string + ']'

    def get_value_string(self, origToNew):
        return str(self.coeff) + '*' + '*'.join(['np.exp(x.value.item('+str(origToNew[i])+'))' for i in self.monoDict.keys()])

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
"""
M = Monomial()
M = M.mono_addCoeff(10)
M = M.mono_multiply(-3,'x',1)
M = M.mono_multiply(3,'x',2)
M = M.mono_multiply(6,'x',3)
M = M.mono_multiply(2,'y',1)
M = M.mono_multiply(1,'y',3)

print M.monoDict
print M.log_of_mono()
"""
