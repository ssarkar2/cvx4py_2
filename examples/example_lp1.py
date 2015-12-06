#linear program

import numpy as np
from cvx4py import cvx4py

c = np.array([[1],[2]])
A = np.array([[1,1,-1,0], [1,-1,0,-1]]);
b = np.array([5,1,0,0])

string = """
cvx_begin
variables x(2)
maximize c'*x
subject to
A'*x <= b
cvx_end
"""

prob = cvx4py(string, 0, locals())
soln = prob.solveProblem();
print soln['x']



