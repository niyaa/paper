import os,sys;
import shutil;
import subprocess;
path=os.getcwd();
import numpy as np;
sys.path.append('/home/nyadav/pyscr');
import ipVar;
rse='nodes=1:tq2:ppn=1';
#rse='nodes=newton-02:ppn=1';
module='module load gmsh/2.9.2';
path=os.getcwd();
os.chdir(path);
betaList=[];
betaList=[0.5]
path=os.getcwd();
print(betaList);
for i in betaList:
    betaPath=path+'/'+str(i);
    if not os.path.exists(betaPath):
    cmd='/home/nyadav/anaconda2/bin/ipython2 manyObj.py '+str(i);
    ipVar.pbs(rse,str(i)+'_'+'ts',module,os.getcwd(),exe);
    subprocess.call("qsub pbs.sh",shell=True);
    os.chdir(path);
    
