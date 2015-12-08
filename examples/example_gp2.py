#ggp

from cvx4py import cvx4py



string = """
cvx_begin gp
variables x y z t1 t2 t4 t5
maximize x*y*z
x*y + y*z <= 100
t1^0.5 <= 50
x*z + (z^0.5)*(y^0.5) <= t1
t2 <= 100
x+z<=t2
x <= 10
y <= 20
z <= 30
cvx_end
"""

'''
GGPLAB code

gpvar x y z             % create three scalar GP variables
constrs = [x <= 10, y <= 20, z <= 30, x*y + y*z <= 100, (x*z + (z)*(y^0.5))^0.5 <= 50, max(x, x+z) <= 100, max(x, (x+2*z)^0.4) <= 100]
[obj_value, solution, status] = gpsolve(x*y*z,constrs, 'max')
assign(solution)
'''

xx = 50
string = """
cvx_begin gp
variables x y z
maximize x*y*z
x*y + y*z <= 100
(x*z + (z)*(y^0.5))^0.5 <= xx
max(x, x+z) <= 100
max(x, (x+2*z)^0.4) <= 100
x <= 10
y <= 20
z <= 30
cvx_end
"""


prob = cvx4py(string, 0, locals())
soln = prob.solveProblem();
print soln