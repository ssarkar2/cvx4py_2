from Monomial import *
import itertools as itr
class Posynomial(object):

    def __init__(self, posyList = None):
        self.posyList = posyList if posyList is not None else []

    def __str__(self):
        return str([str(x) for x in self.posyList])

    def posy_from_mono(self, mono):
        return Posynomial([mono])

    def posy_add_mono(self, mono):
        return Posynomial(self.posyList + [mono])

    def posy_times_posy(self, posy):
        return Posynomial([item[0].mono_times_mono(item[1]) for item in list(itr.product(self.posyList, posy.posyList))])

    def posy_times_mono(self, mono):
        return self.posy_times_posy(Posynomial().posy_from_mono(mono))

    def posy_add_posy(self, posy):
        return Posynomial(self.posyList + posy.posyList)

    def posy_power(self, n):
        return self if n==1 else self.posy_times_posy(self.posy_power(n-1))

    def posy_division_by_mono(self, mono):
        return Posynomial([iter.mono_division_by_mono(mono) for iter in self.posyList])

    def log_sum_exp_form(self, origToNew, newToOrig):
        astr = 'a = np.array(['
        bstr = 'b = np.array(['
        for itr in self.posyList:
            astr = astr + itr.get_array_string(origToNew, newToOrig) + ','
            bstr = bstr + '[np.log(' + str(itr.coeff) +')],'
        astr = astr + '])'
        bstr = bstr + '])'
        return [astr, bstr]



'''
m1 = Monomial()
m1 = m1.mono_multiply(-1,'x',1)
m1 = m1.mono_multiply(1,'y',1)
m1 = m1.mono_addCoeff(6)
print m1  #6y/x

m2 = Monomial()
m2 = m2.mono_multiply(-3,'x',1)
m2 = m2.mono_addCoeff(2)
m2 = m2.mono_raise_to_pow(2)
print m2 #4x^-6


p1 = Posynomial()
p1 = p1.posy_from_mono(m1)
p1 = p1.posy_add_mono(m2)
print p1

print 'xxxx'

m3 = Monomial()
m3 = m3.mono_multiply(3,'x',1)
m3 = m3.mono_multiply(1,'y',1)
m3 = m3.mono_addCoeff(2)
print m3  #2y^2 x^2

m4 = Monomial()
m4 = m4.mono_multiply(-3,'x',1)
m4 = m4.mono_division(2, 'y')
m4 = m4.mono_raise_to_pow(1)
print m4  #y^-2*x^-3

p2 = Posynomial()
p2 = p2.posy_from_mono(m3)
p2 = p2.posy_add_mono(m4)
print p2


p3 = p1.posy_times_posy(p2)
print p3

print m1.mono_times_mono(m2)
print m3.mono_times_mono(m4)
print m1.mono_times_mono(m3)

print p1.posy_power(2)
print p1.posy_division_by_mono(m4)
'''