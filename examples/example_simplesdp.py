from cvx4py import cvx4py
import math
import numpy as np
import cvxopt as cvx
n = 2
C = cvx.matrix(np.array([[1 2] ; [3 4]]))
A1 = cvx.matrix(np.array([[2 3] ;[4 5]))
b1 = 2

string = """
cvx_begin
	variable X(n,n) symmetric
	minimize( trace(C*X) )
	subject to
        trace(A1*X) == b1;
		X >= 0;   %also X = semidefinite(n)
cvx_end
"""


prob = cvx4py(string, 0, locals())
soln = prob.solveProblem();
print soln