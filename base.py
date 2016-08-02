import sys, subprocess;
sys.path.append('/home/nyadav/pyscr');
import ipVar, funcs;
import numpy as np;
import shutil;
import os;
class baseFlow:
    def __init__(self,fileList,filePath,simPara,meshPara):
        self.fileList=fileList;
        self.filePath=filePath;
        self.simPara=simPara;
        self.meshPara=meshPara;
        path=os.getcwd();
        self.pathB=path+'/b';
        if not os.path.exists(self.pathB):
            os.makedirs(self.pathB);
        os.chdir(self.pathB);

        for i in range(0,len(fileList)):
            shutil.copy(filePath[i]+'/'+fileList[i],os.getcwd()+'/'+fileList[i]);


        funcs.simPara(filePath[1],fileList[1],simPara);
        funcs.editGeo(os.getcwd(),os.getcwd(),meshPara[0],meshPara[1],meshPara[2],meshPara[3]);
        subprocess.call("/tools/gmsh/2.9.2/bin/gmsh -2 -order 9 divConv2D.scr" ,shell=True);
        subprocess.call("~/bin/MeshConvert divConv2D.msh geom.xml",shell=True);
        subprocess.call("~/bin/IncNavierStokesSolver geom.xml "+fileList[1]+' > log.txt',shell=True);
        j=funcs.MaxChk(self.pathB);
        args='cp '+'geom_'+str(j)+'.chk'+' geom3D.bse';
        subprocess.call(args,shell=True);
        os.chdir(path);

class distFlow:
    def __init__(self,fileList,filePath,simPara):
        self.fileList=fileList;
        self.filePath=filePath;
        self.simPara=simPara;
        path=os.getcwd();
        pathD=path+'/d';
        if not os.path.exists(pathD):
            os.makedirs(pathD);
        os.chdir(pathD);

        for i in range(0,len(fileList)):
            shutil.copy(filePath[i]+'/'+fileList[i],os.getcwd()+'/'+fileList[i]);

        funcs.simPara(filePath[1],fileList[1],simPara);
        subprocess.call("~/bin/IncNavierStokesSolver geom.xml "+fileList[1]+' > log.txt',shell=True);

class bdFlow:
    def __init__(self,fileList,filePath,simPara):
        self.fileList=fileList;
        self.filePath=filePath;
        self.simPara=simPara;
        path=os.getcwd();
        pathD=path+'/d';
        if not os.path.exists(pathD):
            os.makedirs(pathD);
        os.chdir(pathD);

        for i in range(0,len(fileList)):
            shutil.copy(filePath[i]+'/'+fileList[i],os.getcwd()+'/'+fileList[i]);
       
        funcs.simPara(filePath[1],fileList[1],simPara);
        subprocess.call("~/bin/IncNavierStokesSolver geom.xml "+fileList[1]+' > log.txt',shell=True);

class preHoly:
    def __init__(self,filePath,simPath,f=1):
        self.filePath=filePath;
        self.simPath=simPath;
        [a,b,chkN,energy]=funcs.chkPerUnitTime('bd.xml');
        args='~/bin/FldAddFld -1 1 geom3D.bse'+'geom_'+str(chkN)+'.chk'+' geomHplusD.fld';
        subprocess.call(args,shell=True);
        E1=np.sqrt(1e-17/energy)*f;
        args='~/bin/FldAddFld 1 '+str(E1)+' geom3D.bse geomHplusD.fld geomHplusD.fld';
        subprocess.call(args,shell=True);
        FileList=['geom.xml','bd.xml','geomHplusD.fld'];
        for i in FileList:
            shutil.move(filePath+'/'+i,simPath+'/'+i);

        


    
