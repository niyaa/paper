import subprocess
for i in range(0,4):
    a=0.5+i*0.1;
    arg='ipython2 manyObj.py '+str(a)+' &';
    subprocess.call(arg,shell=True);

for i in range(0,3):
    a=0.05+i*0.1
    arg='ipython2 manyObj.py '+str(a)+' &';
    subprocess.call(arg,shell=True);
for i in range(0,4):
    a=0.3+i*0.05;
    arg='ipython2 manyObj.py '+str(a)+' &';
    subprocess.call(arg,shell=True);


