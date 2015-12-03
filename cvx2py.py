
import picos as pic
import cvxopt as cvx
import math
import numpy as np

#creates a problem and the optimization variables
P = pic.Problem()
	    
ee = 0.05
intra_power = 0.707106781187
Nr = 1
Nt = 4
sq2 = 1.41421356237
sinr = 10
gama = 10
N0 = 1
inter_power = 0.387298334621
h112 = cvx.matrix(np.array([[(1.10921580312-0.874264474953j),],[(-0.43718323106-0.577131975318j),],[(0.0472191988292-1.66305696722j),],[(-1.45654772565-1.76237681556j),],]))
h112 = pic.new_param('h112', h112)
h111 = cvx.matrix(np.array([[(0.0946947559278-0.236827235768j),],[(-0.0622968087533-0.0988014001335j),],[(1.18398553854-0.11064849353j),],[(0.518762601924-0.0424897755693j),],]))
h111 = pic.new_param('h111', h111)
h221 = cvx.matrix(np.array([[(0.283644888399+0.375625089654j),],[(0.579690516352-0.494490802416j),],[(0.0139632243689-0.64582043198j),],[(0.419073409041-0.198125375802j),],]))
h221 = pic.new_param('h221', h221)
h222 = cvx.matrix(np.array([[(0.438966598707+0.329435249682j),],[(-0.392175758814+0.757981878088j),],[(-0.0777160229203+0.196684295657j),],[(-1.11266113986-0.313845603596j),],]))
h222 = pic.new_param('h222', h222)
I = cvx.matrix(np.array([[1.0,0.0,0.0,0.0,],[0.0,1.0,0.0,0.0,],[0.0,0.0,1.0,0.0,],[0.0,0.0,0.0,1.0,],]))
I = pic.new_param('I', I)
h122 = cvx.matrix(np.array([[(-0.171636792167-0.536643525694j),],[(0.385495944495+0.21605087408j),],[(0.303042723922-0.51714935424j),],[(0.309991385243+0.690950212787j),],]))
h122 = pic.new_param('h122', h122)
h121 = cvx.matrix(np.array([[(-0.240643015796-0.926635968539j),],[(-0.0704546904349+0.191472492601j),],[(-0.00141199057604-0.288136331605j),],[(-0.360832148421+0.118551020343j),],]))
h121 = pic.new_param('h121', h121)
h211 = cvx.matrix(np.array([[(0.417155081021+0.0379506052073j),],[(0.184031386309+0.136943890617j),],[(-0.00308560295212+0.247970878724j),],[(-0.296449293819-0.65905819439j),],]))
h211 = pic.new_param('h211', h211)
h212 = cvx.matrix(np.array([[(-0.00926321178832-0.330860255805j),],[(0.0468869362843+0.94195927056j),],[(-0.366382211667-0.148096234076j),],[(-0.521466859137+0.646176216911j),],]))
h212 = pic.new_param('h212', h212)

w11 = P.add_variable('w11',(Nt,Nt),'hermitian')
P.add_constraint( w11>>0 )
w12 = P.add_variable('w12',(Nt,Nt),'hermitian')
P.add_constraint( w12>>0 )
w21 = P.add_variable('w21',(Nt,Nt),'hermitian')
P.add_constraint( w21>>0 )
w22 = P.add_variable('w22',(Nt,Nt),'hermitian')
P.add_constraint( w22>>0 )
beta211 = P.add_variable('beta211',1, lower=0)
beta212 = P.add_variable('beta212',1, lower=0)
beta121 = P.add_variable('beta121',1, lower=0)
beta122 = P.add_variable('beta122',1, lower=0)
apha111 = P.add_variable('apha111',1, lower=0)
apha112 = P.add_variable('apha112',1, lower=0)
apha121 = P.add_variable('apha121',1, lower=0)
apha122 = P.add_variable('apha122',1, lower=0)
apha221 = P.add_variable('apha221',1, lower=0)
apha222 = P.add_variable('apha222',1, lower=0)
apha211 = P.add_variable('apha211',1, lower=0)
apha212 = P.add_variable('apha212',1, lower=0)
P.set_objective('min','I'|w11+w12+w21+w22)
P.add_constraint( ( (w11/gama-w12+apha111*I & (w11/gama-w12).H*h111) // (h111.H*(w11/gama-w12) & -beta211-N0-apha111*ee**2+h111.H*(w11/gama-w12)*h111) )>>0 ) 
P.add_constraint( ( (w12/gama-w11+apha112*I & (w12/gama-w11).H*h112) // (h112.H*(w12/gama-w11) & -beta212-N0-apha112*ee**2+h112.H*(w12/gama-w11)*h112) )>>0 ) 
P.add_constraint( ( (w21/gama-w22+apha221*I & (w21/gama-w22).H*h221) // (h221.H*(w21/gama-w22) & -beta121-N0-apha221*ee**2+h221.H*(w21/gama-w22)*h221) )>>0 ) 
P.add_constraint( ( (w22/gama-w21+apha222*I & (w22/gama-w21).H*h222) // (h222.H*(w22/gama-w21) & -beta122-N0-apha222*ee**2+h222.H*(w22/gama-w21)*h222) )>>0 ) 
P.add_constraint( ( (-w11-w12+apha121*I & -(w11+w12).H*h121) // (-h121.H*(w11+w12) & beta121-apha121*ee**2-h121.H*(w11+w12)*h121) )>>0 ) 
P.add_constraint( ( (-w11-w12+apha122*I & -(w11+w12).H*h122) // (-h122.H*(w11+w12) & beta122-apha122*ee**2-h122.H*(w11+w12)*h122) )>>0 ) 
P.add_constraint( ( (-w21-w22+apha211*I & -(w21+w22).H*h211) // (-h211.H*(w21+w22) & beta211-apha211*ee**2-h211.H*(w21+w22)*h211) )>>0 ) 
P.add_constraint( ( (-w21-w22+apha212*I & -(w21+w22).H*h212) // (-h212.H*(w21+w22) & beta212-apha212*ee**2-h212.H*(w21+w22)*h212) )>>0 ) 

#display the problem
print P

#call to the solver cvxopt
sol = P.solve(solver='cvxopt',verbose = 1)
print 'optimal value:'
print P.obj_value()

f = open('soln_sdp.txt', 'w')
f.write('objval: ' + str(P.obj_value()) + '\n')
f.write('w11: ' +w11.__str__().replace('\n', ';')+ '\n') 
f.write('w12: ' +w12.__str__().replace('\n', ';')+ '\n') 
f.write('w21: ' +w21.__str__().replace('\n', ';')+ '\n') 
f.write('w22: ' +w22.__str__().replace('\n', ';')+ '\n') 
f.write('beta211: ' +beta211.__str__().replace('\n', ';')+ '\n') 
f.write('beta212: ' +beta212.__str__().replace('\n', ';')+ '\n') 
f.write('beta121: ' +beta121.__str__().replace('\n', ';')+ '\n') 
f.write('beta122: ' +beta122.__str__().replace('\n', ';')+ '\n') 
f.write('apha111: ' +apha111.__str__().replace('\n', ';')+ '\n') 
f.write('apha112: ' +apha112.__str__().replace('\n', ';')+ '\n') 
f.write('apha121: ' +apha121.__str__().replace('\n', ';')+ '\n') 
f.write('apha122: ' +apha122.__str__().replace('\n', ';')+ '\n') 
f.write('apha221: ' +apha221.__str__().replace('\n', ';')+ '\n') 
f.write('apha222: ' +apha222.__str__().replace('\n', ';')+ '\n') 
f.write('apha211: ' +apha211.__str__().replace('\n', ';')+ '\n') 
f.write('apha212: ' +apha212.__str__().replace('\n', ';')+ '\n') 
f.close()
