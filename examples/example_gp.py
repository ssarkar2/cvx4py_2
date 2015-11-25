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

n=2
string = """
cvx_begin gp
variables x y(n) x  %the extra x is to test that parser should give error if we redeclare a variable
variable z
maximize (x*x)*x^2
x*z == 1
x + y(1)*y(2)*z + y(1) <= 4
3*y(1)*z <= 1
cvx_end
"""
'''
string = string = """
cvx_begin gp
variables x y(n) x  %the extra x is to test that parser should give error if we redeclare a variable
variable z
maximize x*x*x^2

cvx_end
"""
'''
prob = cvx4py(string, 0, locals())
prob.solveProblem();