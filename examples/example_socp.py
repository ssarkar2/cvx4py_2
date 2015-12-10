#robust linear programming
#sec 4.2.2 of Boyd's book

import numpy as np
from cvx4py import cvx4py

c = np.array([[1],[2]])
A = np.array([[1,-1,0], [-1,0,-1]]);
b = np.array([1,0,0])
a1 = np.array([[1],[1]]) ; b1 = 5
P1 = np.array([[1,2],[2,1]])


string = """
cvx_begin
variables x(2)
maximize c'*x
subject to
A'*x <= b
a1'*x + norm(P1*x) <= b1
cvx_end
"""

prob = cvx4py(string, 0, locals())
soln = prob.solveProblem();
print soln['x']



