import os,sys;
from output import *;
import shutil;
import subprocess;
path=os.getcwd();
import numpy as np;
from glob import glob;
import time
sys.path.append('/home/nyadav/pyscr');
import ipVar;
rse='nodes=1:ppn=1';
#rse='nodes=newton-02:ppn=1';
module='module load gmsh/2.9.2';
cwd=os.getcwd();
ReList=[70,80,100,200,400,600,800,1000,1200,1400,1600,1800,2000]

out=Output();
out.alpha, out.S, out.betaCr, out.Re=np.loadtxt('/home/nyadav/test2/new.txt',usecols=(0,1,2,3),unpack=True);
alpha=float(cwd.split('/')[-2]);
sval=float(cwd.split('/')[-1]);
betas=out.betaCr[(out.alpha==alpha)&(out.S==sval)];
print(betas);
print(os.getcwd());
path=os.getcwd();
for i in betas:
    for j in ReList:
        betaPath=path+'/'+str(i);
        cmd=[];
        time.sleep(3)
        cmd.append('/home/nyadav/anaconda2/bin/ipython2 /home/nyadav/pyscr/manyObj3.py '+str(i)+' '+str(j));
        crdir=os.getcwd();
        ipVar.pbs(rse,path+str(i),module,os.getcwd(),cmd);
        subprocess.call("qsub pbs.sh",shell=True);
        os.chdir(path);
    
