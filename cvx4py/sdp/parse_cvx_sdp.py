def parse_cvx_sdp(cvxstring, locals, filename):
    import cvxopt as cvx
    lines = [line.strip('\n') for line in cvxstring.split('\n')]
    sdp = open(filename,'w')
    string = """
import picos as pic
import cvxopt as cvx
import math
import numpy as np

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

    sdp.write("%s\n" % string)
    flag = 0
    varnames = []
    for line in lines:
        if line.strip():
            if 'cvx_begin' in line:
                continue
            if 'cvx_end' in line:
                break
            line = line.lstrip()
            line = line.split('%')[0]
            line = line.replace('\'', '.H')
            line = line.replace('^', '**')
            line = line.replace(';','')

            if flag == 0:
                if 'variable ' in line:
                    if 'hermitian' in line:
                        parts = line.split(' ')
                        [var,param] = parts[1].split('(')
                        param = param.split(',')[0]
                        sdp.write("%s = P.add_variable('%s',(%s,%s),'hermitian')\n" % (var, var,param,param))
                        varnames = varnames + [var]
                        if 'semidefinite' in line:
                            sdp.write("P.add_constraint( %s>>0 )\n" % var )
                    elif 'symmetric' in line:
                        parts = line.split(' ')
                        [var,param] = parts[1].split('(')
                        param = param.split(',')[0]
                        sdp.write("%s = P.add_variable('%s',(%s,%s),'symmetric')\n" % (var,var,param,param))
                        varnames = varnames + [var]
                        if 'semidefinite' in line:
                            sdp.write("P.add_constraint( %s>>0 )\n" % var )
                    elif 'nonnegative' in line:
                        parts = line.split(' ')
                        var = parts[1]
                        sdp.write("%s = P.add_variable('%s',1, lower=0)\n" % (var,var))
                        varnames = varnames + [var]
                    elif 'complex' in line:
                        parts = line.split(' ')
                        if '(' in line:
                            [var,param] = parts[1].split('(')
                            param = param.split(',')[0]
                            sdp.write("%s = P.add_variable('%s',(%s,%s),'complex')\n" % (var, var,param,param))
                            varnames = varnames + [var]
                        else:
                            var = parts[1]
                            sdp.write("%s = P.add_variable('%s',1, 'complex')\n" % (var,var))
                            varnames = varnames + [var]
                    else:
                        parts = line.split(' ')
                        if '(' in line:
                            [var,param] = parts[1].split('(')
                            param = param.split(',')[0]
                            sdp.write("%s = P.add_variable('%s',(%s,%s))\n" % (var, var,param,param))
                            varnames = varnames + [var]
                        else:
                            var = parts[1]
                            sdp.write("%s = P.add_variable('%s',1)\n" % (var,var))
                            varnames = varnames + [var]
                elif 'variables' in line:
                    parts = line.split(' ')[1:]
                    for i in range(len(parts)):
                        sdp.write("%s = P.add_variable('%s',1)\n" % (parts[i],parts[i]))
                        varnames = varnames + [var]
                elif 'minimize' in line or 'maximize' in line:
                    if 'min' in line:
                        fun = 'min';
                    else:
                        fun = 'max'
                    if 'trace' in line:
                        parts = line.split('trace(')
                        parts = parts[1:]
                        obj = ''
                        for i in range(len(parts)):
                            obj += parts[i].split(')')[0]
                            if i < len(parts)-1 and len(parts)>1:
                                obj += '+'
                        sdp.write("P.set_objective('%s','I'|%s)\n" % (fun, obj))
                    else:
                        if 'min' in fun:
                            obj = line.split('minimize')[1].split('(',1)[1].rsplit(')',1)[0]
                        else:
                            obj = line.split('maximize')[1].split('(',1)[1].rsplit(')',1)[0]
                        sdp.write("P.set_objective('%s',%s)\n" % (fun, obj))
                elif 'subject' in line:
                    flag = 1
            else:
                if '==' in line:
                    parts = line.split('==')
                    if 'trace' in parts[0]:
                        tmp = parts[0]
                        param = parts[1]
                    else:
                        tmp = parts[1]
                        param = parts[0]
                    var = tmp.split('trace(')[1].split(')')[0]
                    sdp.write("P.add_constraint('I'|%s==%s)\n" % (var,param))
                if '[' in line:
                    parts = line.split()
                    l = parts[0].split('[')[1]
                    r = parts[1].split('...')[0]
                    sdp.write("P.add_constraint( ( (%s & %s) " % (l,r))
                elif ']' in line:
                    parts = line.split()
                    l = parts[0]
                    r = parts[1].split(']')[0]
                    sdp.write("// (%s & %s) )>>0 ) \n" % (l,r))
                elif '>=' in line:
                    parts = line.split('>=')
                    var = parts[0]
                    sdp.write("P.add_constraint(%s >>0 ) \n" % var)
                elif 'semidefinite' in line:
                    parts = line.split('==')
                    if 'semidefinite' in parts[0]:
                        var = parts[1]
                    else:
                        var = parts[0]
                    sdp.write("P.add_constraint( %s>>0 )\n" % var )

	string = '''
#display the problem
#print P

#call to the solver cvxopt
sol = P.solve(solver='cvxopt',verbose = 1)
print 'optimal value:'
print P.obj_value()

f = open('soln_sdp.txt', 'w')
f.write('objval: ' + str(P.obj_value()) + '\\n')
'''

    for itr in varnames:
        string = string + 'f.write(' + '\'' + itr + ': \' +' + itr + '.__str__().replace(\'\\n\', \';\')+ \'\\n\') ' + '\n'
    string = string + 'f.close()'

    sdp.write("%s\n" % string)
    sdp.close()












