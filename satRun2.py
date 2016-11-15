import os, sys, subprocess;
sys.path.append('/home/nyadav/pyscr/');
import ipVar, funcs;
from case import *;
from MonkeyPatch import *;
import xml.etree.ElementTree as ET;
from glob import glob;
pathA=os.getcwd();
FileList=['geom.xml','bd.xml','geomBplusD.fld'];
FilePath=pathA+'/'+'bd.xml';
tree=ET.parse(FilePath,OrderedXMLTreeBuilder());
root=tree.getroot();
Re=int(root[1][1][5].text.split('=')[-1]);
a=[-1,-1];

os.chdir(str(Re));
FilePath=os.getcwd()+'/'+'bd.xml';
tree=ET.parse(FilePath,OrderedXMLTreeBuilder());
root=tree.getroot();
Re=int(root[1][1][5].text.split('=')[-1]);
os.chdir(pathA);
ReMult=[0.4,0.8,1.6,3.2];

for f in ReMult:   
    Re=int(Re+Re*f);
    if not os.path.exists(str(Re)):
        os.makedirs(str(Re));
    os.chdir(str(Re));
    pathB=os.getcwd();
    time=500
    para=[0.005,time,'FinalTime/TimeStep',Re,64,0.4,'','','','1'];
    funcs.CopyFile(pathA,os.getcwd(),FileList);
    funcs.simPara(os.getcwd(),'bd.xml',para);
    subprocess.call('mpirun -np 32 /home/nyadav/.sg/IncNavierStokesSolver --npz 32 geom.xml bd.xml',shell=True);    
    funcs.simPara(os.getcwd(),'bd.xml',para);
    if not os.path.exists(str(2)):
        os.makedirs(str(2));
    os.chdir(str(2));
    funcs.CopyFile(pathB,os.getcwd(),FileList);
    funcs.ICFile(pathB,os.getcwd(),'geom.fld','bd.xml');
    subprocess.call('mpirun -np 32 /home/nyadav/.sg/IncNavierStokesSolver --npz 32 geom.xml bd.xml',shell=True);    
    
    subprocess.call('rm -r IC.bse',shell=True)
    subprocess.call('mv geom.fld IC.bse',shell=True);

    funcs.addEnergyFile(os.getcwd(),'energyfile.mdl');
    bc=funcs.MaxChk(os.getcwd());
    ac=funcs.MaxChk(pathB);
    funcs.moveChk(os.getcwd(),pathB,ac,bc);
    time=500
    while(not ipVar.CheckEnergySat('EnergyFile.mdl')):
        para=[0.005,time,'FinalTime/TimeStep',Re,64,0.4,'','','','1'];
        funcs.simPara(os.getcwd(),'bd.xml',para);
        funcs.ICFile(pathB,os.getcwd(),'geom.fld','bd.xml');

        subprocess.call('mpirun -np 32 /home/nyadav/.sg/IncNavierStokesSolver --npz 32 geom.xml bd.xml',shell=True);    
        subprocess.call('rm -r IC.bse',shell=True)
        subprocess.call('mv geom.fld IC.bse',shell=True);
        funcs.addEnergyFile(os.getcwd(),'energyfile.mdl');
        bc=funcs.MaxChk(os.getcwd());
        ac=funcs.MaxChk(pathB);
        funcs.moveChk(os.getcwd(),pathB,ac,bc);

    os.chdir(pathA);





