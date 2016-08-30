import manySim3;
import sys;
import os;
import subprocess;

first_arg=sys.argv[1];
a=[];
a.append(float(first_arg));
print(a)
cwd=os.getcwd();
subprocess.call('rm bd.xml',shell=True);
args='cp /home/nyadav/pyscr/bd.xml'+' '+cwd;
subprocess.call(args,shell=True); 
alpha=float(cwd.split('/')[-2]);
sval=float(cwd.split('/')[-1]);
b=manySim3.CriticalRe(a,alpha,sval)
b.CreForBeta3();
