from cvx4py import cvx4py

alpha = 0.5; beta = 2; gamma = 0.5; delta = 2;
Awall = 100
Afloor = 2000

string = """
cvx_begin gp
    variables w h d
    maximize( w * h * d )
    subject to
        2*(h*w+h*d) <= Awall;
        w*d <= Afloor;
        alpha <= h/w >= beta;
        gamma <= d/w <= delta;
cvx_end
"""

string = """
cvx_begin gp
x  +y <= x*y
cvx_end
"""

prob = cvx4py(string, 0, locals())
prob.solveProblem();