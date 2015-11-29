def parse_cvx_sdp(cvxstring, locals, filename):
    import re
    import cvxopt as cvx
    dh = open(filename,'w')
    string = """
import picos as pic
import cvxopt as cvx
import math
import numpy as np
Nt = 4
Nr = 1
sinr=10
gama=10**(sinr/10)
ee=0.05
N0=1
sq2=math.sqrt(2)
intra_power = math.sqrt(1) / sq2
inter_power = math.sqrt(0.3)/ sq2

#creates a problem and the optimization variables
P = pic.Problem()
    """
    string = string + '\n'
    numstring = ''
    mtxstring = ''
    #print locals
    for itr in locals.keys():
        if isinstance(locals[itr], (int, long, float, complex)):
            numstring = numstring + itr + ' = ' + str(locals[itr]) +'\n'
        elif isinstance(locals[itr], cvx.matrix):
            mtx = locals[itr]
            numpystring = 'np.array(['
            for row in range(mtx.size[0]):
                numpystring = numpystring + '['
                for col in range(mtx.size[1]):
                    numpystring = numpystring + str(mtx[row*mtx.size[1]+col]) + ','
                numpystring = numpystring + '],'
            numpystring = numpystring + '])'
            mtxstring = mtxstring + itr + ' = cvx.matrix('+numpystring+')\n'
            mtxstring = mtxstring + itr + ' = pic.new_param(\'' + itr + '\', ' + itr + ')\n'
    string = string + numstring
    string = string + mtxstring

    dh.write("%s\n" % string)
    lines = [line.strip('\n') for line in cvxstring.split('\n')] #[line.rstrip('\n') for line in open('cvx_sdp.txt','r')]
    flag = 0
    varnames = []
    for line in lines:
    	if flag == 0:
    		if line.endswith('sdp'):
    			continue
    		elif line.startswith('variable'):
    			if 'semidefinite' in line:
    				parts = line.split(' ')
    				[var,param] = parts[1].split('('); varnames = varnames + [var]
    				param = param.split(',')[0]
    				dh.write("%s = P.add_variable('%s',(%s,%s),'hermitian')\n" % (var, var,param,param))
    				dh.write("P.add_constraint( %s>>0 )\n" % var )
    			elif 'nonnegative' in line:                                                                 #TO do : else (if  nonnegative is not there)
    				parts = line.split(' ')
    				var = parts[1]
    				dh.write("%s = P.add_variable('%s',1, lower=0)\n" % (var,var))
    		elif line.startswith('minimize'):
    			parts = line.split('trace(')
    			parts = parts[1:]
    			obj = ''
    			for i in range(len(parts)):
    				obj += parts[i].split(')')[0]
    				if i < len(parts)-1:
    					obj += '+'
    			dh.write("P.set_objective('min','I'|%s)\n" % obj)
    		elif line.startswith('subject'):
    			flag = 1
    	else:
    		if 'cvx_end' in line:
    			break
    		if line.strip():
    			if '\'' in line:
    				line = line.replace('\'', '.H')
    			if '^' in line:
    				line = line.replace('^', '**')
    			parts = line.split()
    			if '>=' in line:
    				l = parts[0]
    				r = parts[1].split(']')[0]
    				dh.write("// (%s & %s) )>>0 ) \n" % (l,r))
    			else:
    				l = parts[0].split('[')[1]
    				r = parts[1].split(';')[0]
    				dh.write("P.add_constraint( ( (%s & %s) " % (l,r))

    string = '''
#display the problem
print P

#call to the solver cvxopt
sol = P.solve(solver='cvxopt',verbose = 1)
print 'optimal value:'
print P.obj_value()
    '''
    print varnames

    dh.write("%s\n" % string)
    dh.close()










