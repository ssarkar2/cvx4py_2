from cvx4py import cvx4py


string = """
cvx_begin sdp
cvx_end
"""



prob = cvx4py(string, 0, locals())
soln = prob.solveProblem();
print soln