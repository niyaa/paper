import os,sys;
import shutil;
import subprocess;
path=os.getcwd();
import numpy as np;
from glob import glob;
import time
sys.path.append('/home/nyadav/pyscr');
import ipVar;
rse='nodes=1:tq3:ppn=1';
#rse='nodes=newton-02:ppn=1';
module='module load gmsh/2.9.2';
path=os.getcwd();
os.chdir(path);
betaList=[]
#betaList=[0.1,0.3,0.2,0.25 ,0.35,0.4,0.45,0.5,0.6]
#betaList=[0.85,0.9,1,1.1,1.2,1.3,1.4,1.5,1.6];
#betaList=[0.05,0.25 ,0.35,0.6,0.8,0.15 ,0.3,0.4,0.5,0.7,0.1, 0.8, 0.9,1,1.1,1.2,1.3,1.4,1.5,1.6]
#betaList=[0.7,0.75,0.05]
#for i in range(1,4):
#    betaList.append(0.66+0.04*i)
Betas=glob("*/");
for ii in Betas:
    betaList.append(float(ii.split('/')[0]));


path=os.getcwd();
print(betaList);
for i in betaList:
    betaPath=path+'/'+str(i);
    cmd=[];
    time.sleep(1)
    cmd.append('/home/nyadav/anaconda2/bin/ipython2 /home/nyadav/pyscr/manyObj2.py '+str(i));
    crdir=os.getcwd();
    ipVar.pbs(rse,path+str(i),module,os.getcwd(),cmd);
    subprocess.call("qsub pbs.sh",shell=True);
    os.chdir(path);
    
