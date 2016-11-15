import manySim3hyp;
import sys;
import os;
import subprocess;

first_arg=sys.argv[1];
a=[];
a.append(float(first_arg));
print(a)
cwd=os.getcwd();
alpha=float(cwd.split('/')[-2]);
sval=float(cwd.split('/')[-1]);
os.chdir(str(a[0]));

