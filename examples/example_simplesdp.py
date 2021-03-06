from cvx4py import cvx4py
import cvxopt as cvx

n = 3
C = cvx.matrix([[1,2,3] , [2,9,0], [3,0,7]])
A1 = cvx.matrix([[1,0,1] ,[0,3,7],[1,7,5]])
b1 = 11
A2 = cvx.matrix([[0,2,8] ,[2,6,0],[8,0,4]])
b2 = 19


string = """
cvx_begin sdp
	variable X(n,n) symmetric
	minimize( trace(C*X) )
	subject to
		trace(A1*X) == b1;
		trace(A2*X) == b2;
		X >= 0;  
cvx_end
"""

prob = cvx4py(string, 0, locals())
soln = prob.solveProblem();
print soln
