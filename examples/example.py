#example file.

#import our framework

import numpy as np
from cvx4py import cvx4py

string = """
cvx_begin
variable d
minimize d
5 >= d >= 0
cvx_end
"""

A = np.array([[ 1., 2.], [ 0., 0.], [ 1., 3.]])
prob = cvx4py(string, 0, locals())
prob.solve();


#prob = cvx4py('myfile.cvx', 1, locals())
#prob.solve();


