#example file.

#import our framework

import numpy as np
from cvx4py import cvx4py

#works ok
#vaiable with brackets d(1) or d both work
#comments work
#chanined constraints work
#dual variable declaration
#multiple variable declation
#multiple constraints
#commas and semicolons separating statements
string = """
cvx_begin
variable d(1) % hello0
minimize d
5 >= d >= 0
cvx_end
"""


#this work
'''
tests the keywords variable and variables
tests dual variable keywords
allows qq(2) (multi dimension variable)
allows parameters (a)
chained constraints and dual constraints
separation of statements by ; and ,
inequalities involving multivalues vars (q >= 0)
ineqs with parameters (a*qq >= 0)
identify gp mode
'''
#doesnt work
'''
x >= 0 : l  (this kind of dual variable pairings)
'''
string = """
cvx_begin gp, variable d
variables pp(1) qq(2)
dual variable dd
dual variables xx yy
minimize d + (pp) + a*qq
4 >= d >= 1
dd: d >= 0
pp >= 0 ; (pp >= 1)
pp >= 2, pp >= 3 %:yy
pp >= 4 %: xx
a*qq >= 0
qq>=0,
cvx_end
"""


#to do: test more and find out what doesnt work and fix it


A = np.array([[ 1., 2.], [ 0., 0.], [ 1., 3.]])
a = np.array([[1, 2]])
prob = cvx4py(string, 0, locals())
prob.solve();


#prob = cvx4py('myfile.cvx', 1, locals())
#prob.solve();


