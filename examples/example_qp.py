#example file.

#import our framework

import numpy as np
from cvx4py import cvx4py

A = np.array([[ 0., 0.], [ 1., 2.], [ 2., 1.], [ 2., 2.]])
b = np.array([[0],[9],[7],[9]])

string = """
cvx_begin
variables x(2)
minimize norm(A*x - b)
cvx_end
"""

prob = cvx4py(string, 0, locals())
soln = prob.solveProblem();
print soln['x']



