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

#this also works:
string = """
cvx_begin
variable d
variable pp(1)
dual variable dd
minimize d + pp
dd: d >= 0
pp >= 0 ; pp >= 1
pp >= 2, pp >= 3
pp >= 4
cvx_end
"""


#to do: test more and find out what doesnt work and fix it





A = np.array([[ 1., 2.], [ 0., 0.], [ 1., 3.]])
prob = cvx4py(string, 0, locals())
prob.solve();


#prob = cvx4py('myfile.cvx', 1, locals())
#prob.solve();


