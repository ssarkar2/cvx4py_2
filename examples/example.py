#example file.

#import our framework

import numpy as np
from cvx4py import cvx4py

#works ok
#vaiable with brackets d(1) or d both work
#comments work
#chanined constraints work
#dual variable declaration
#multiple variable declation
#multiple constraints
#commas and semicolons separating statements
string = """
cvx_begin
variable d(1) % hello0
minimize d
5 >= d >= 0
cvx_end
"""


#this work
'''
tests the keywords variable and variables
tests dual variable keywords
allows qq(2) (multi dimension variable)
allows parameters (a)
chained constraints and dual constraints
separation of statements by ; and ,
inequalities involving multivalues vars (q >= 0)
ineqs with parameters (a*qq >= 0)
identify gp mode
variable x(n), or variable x(n,m), where n and m are constants declared in locals()
'''
#doesnt work
'''
1) x >= 0 : l  (this kind of dual variable pairings)
2) ... for continuing same statement to multiple lines
for example:
     c(1) ... this is a comment
       ==    1;
'''
string = """
cvx_begin, variable d
variables pp(1) qq(2)
dual variable dd
dual variables xx yy
minimize d + (pp) + a*qq
4 >= d >= 1
dd: d >= 0
pp >= 0 ; (pp >= 1)
pp >= 2, pp >= 3 %:yy
pp >= 4 %: xx
a*qq >= 0
qq>=0, exp(d+d) > exp(4)
cvx_end
"""


string = """
cvx_begin, variable d(2)
variable c
minimize sum(d) + max(d) + abs(norm2(d))
%exp(d+d) > exp(4)
-a*d > 7
sum(d) <= 4
cvx_end
"""

zz=2
string = """
cvx_begin,
variable d(zz)
variable xxxx(zz,zz)
variables c b(2)
dual variable dd
minimize  abs(sum(d)) + max(d) + sum(abs(d))
%d <= 0
%exp(d+d) > exp(4)
a*d >= 7 %: dd
abs(d) <= 4
cvx_end
"""

'''
string = """
cvx_begin gp
    variables w h d
    maximize(w) %w * h * d
    %subject to
     %   2*(h*w+h*d) <= Awall;
      %  w*d <= Afloor;
       % alpha <= h/w >= beta;
        %gamma <= d/w <= delta;
cvx_end
"""
'''

Awall = 4
Afloor = 2
alpha = 0.5; beta = 2; gamma = 0.5; delta = 2; #https://github.com/cvxr/CVX/blob/master/examples/gp_tutorial/max_volume_box.m

#to do: test more and find out what doesnt work and fix it


A = np.array([[ 1., 2.], [ 0., 0.], [ 1., 3.]])
a = np.array([[1, 2]])
prob = cvx4py(string, 0, locals())
prob.solveProblem();


#prob = cvx4py('myfile.cvx', 1, locals())
#prob.solve();


