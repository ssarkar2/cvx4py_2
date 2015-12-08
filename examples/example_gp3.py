#ggp

from cvx4py import cvx4py



alpha = 0.5; beta = 2; gamma = 0.5; delta = 2;
Awall = 100
Afloor = 2000

string = """
cvx_begin gp
        variables w h d
        dual variables d1 d2 d3
        maximize w*h*d
        d1: 2*(h*w+h*d) <= Awall;
        d2: w*d <= Afloor;
        d3: d < 10
cvx_end
"""


prob = cvx4py(string, 0, locals())
soln = prob.solveProblem();
print soln