from cvx4py import cvx4py
import math
import numpy as np
import cvxopt as cvx
Nt = 4
Nr = 1
sinr=10
gama=10**(sinr/10)
ee=0.05
N0=1
sq2=math.sqrt(2)
intra_power = math.sqrt(1) / sq2
inter_power = math.sqrt(0.3)/ sq2
I = cvx.matrix(np.identity(Nt))


h111 = intra_power*(cvx.normal (Nt,Nr) +1j*cvx.normal (Nt,Nr))
h112 = intra_power*(cvx.normal (Nt,Nr) +1j*cvx.normal (Nt,Nr))
h121 = inter_power*(cvx.normal (Nt,Nr) +1j*cvx.normal (Nt,Nr))
h122 = inter_power*(cvx.normal (Nt,Nr) +1j*cvx.normal (Nt,Nr))

h221 = intra_power*(cvx.normal (Nt,Nr) +1j*cvx.normal (Nt,Nr))
h222 = intra_power*(cvx.normal (Nt,Nr) +1j*cvx.normal (Nt,Nr))
h211 = inter_power*(cvx.normal (Nt,Nr) +1j*cvx.normal (Nt,Nr))
h212 = inter_power*(cvx.normal (Nt,Nr) +1j*cvx.normal (Nt,Nr))

string = """
cvx_begin sdp
variable w11(Nt,Nt) hermitian semidefinite;
variable w12(Nt,Nt) hermitian semidefinite;
variable w21(Nt,Nt) hermitian semidefinite;
variable w22(Nt,Nt) hermitian semidefinite;

variable beta211 nonnegative;
variable beta212 nonnegative;
variable beta121 nonnegative;
variable beta122 nonnegative;
variable apha111 nonnegative;
variable apha112 nonnegative;
variable apha121 nonnegative;
variable apha122 nonnegative;
variable apha221 nonnegative;
variable apha222 nonnegative;
variable apha211 nonnegative;
variable apha212 nonnegative;

minimize(trace(w11)+trace(w12)+trace(w21)+trace(w22));
subject to
sym([w11/gama-w12+apha111*I     (w11/gama-w12)'*h111; ...
h111'*(w11/gama-w12)       -beta211-N0-apha111*ee^2+h111'*(w11/gama-w12)*h111])>=0;

sym([w12/gama-w11+apha112*I     (w12/gama-w11)'*h112; ...
h112'*(w12/gama-w11)        -beta212-N0-apha112*ee^2+h112'*(w12/gama-w11)*h112])>=0;

sym([w21/gama-w22+apha221*I     (w21/gama-w22)'*h221; ...
h221'*(w21/gama-w22)        -beta121-N0-apha221*ee^2+h221'*(w21/gama-w22)*h221])>=0;

sym([w22/gama-w21+apha222*I     (w22/gama-w21)'*h222; ...
h222'*(w22/gama-w21)        -beta122-N0-apha222*ee^2+h222'*(w22/gama-w21)*h222])>=0;

sym([-w11-w12+apha121*I       -(w11+w12)'*h121; ...
-h121'*(w11+w12)        beta121-apha121*ee^2-h121'*(w11+w12)*h121])>=0;

sym([-w11-w12+apha122*I       -(w11+w12)'*h122; ...
-h122'*(w11+w12)        beta122-apha122*ee^2-h122'*(w11+w12)*h122])>=0;

sym([-w21-w22+apha211*I       -(w21+w22)'*h211; ...
-h211'*(w21+w22)        beta211-apha211*ee^2-h211'*(w21+w22)*h211])>=0;

sym([-w21-w22+apha212*I       -(w21+w22)'*h212; ...
-h212'*(w21+w22)        beta212-apha212*ee^2-h212'*(w21+w22)*h212])>=0;
cvx_end
"""

prob = cvx4py(string, 0, locals())
soln = prob.solveProblem();
print soln