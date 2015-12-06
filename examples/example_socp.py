#robust linear programming
#sec 4.2.2 of Boyd's book

import numpy as np
from cvx4py import cvx4py

c = np.array([[1],[2]])
A = np.array([[1,1,-1,0], [1,-1,0,-1]]);
b = np.array([5,1,0,0])
a1 = np.array([[1],[1]]) ; b1 = 5
a2 = np.array([[1],[-1]]) ; b2 = 1
a3 = np.array([[-1],[0]]) ; b3 = 0
a4 = np.array([[0],[-1]]) ; b4 = 0
P1 = np.array([[1,2],[2,1]])


string = """
cvx_begin
variables x(2)
maximize c'*x
subject to
a2'*x <= b2
a3'*x <= b3
a4'*x <= b4
%a1'*x <= b1
a1'*x + norm(P1*x) <= b1
cvx_end
"""

prob = cvx4py(string, 0, locals())
soln = prob.solveProblem();
print soln['x']



