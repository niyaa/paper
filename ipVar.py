    # -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 17:08:18 2016

@author: niya
"""
from MonkeyPatch import *;
import xml.etree.ElementTree as ET;
from glob import glob;
import sys, os, shutil;
import os, extractdata;
import numpy as np;
from case import *;
from decimal import Decimal; 
import pickle; 
import subprocess;
from scipy.interpolate import UnivariateSpline;
import numpy as np;
from scipy.interpolate import interp1d;

def CheckEnergy(filename):
    energy = np.loadtxt(filename,skiprows=1);
    a=energy[-1,-1];
    if((a > 1e-9) or ( a < 1e-20)):   return 0;
    else: return 1;

def PbsChange(path,name):
    os.chdir('/home/nyadav/pbs');
    f1=open('/home/nyadav/pbs/jobBezmpi.sh','r');
    d=f1.readlines();
    d[2]='#PBS -N '+name;
    d[6]='cd '+path;
    f1.close();
    # subprocess('rm /home/nyadav/pbs/jobBezmpi.sh',shell=True);
    f1=open('/home/nyadav/pbs/abc.sh','w');	
    f1.writelines(d);
    f1.close();

    subprocess("chmod" "u+x" "/home/nyadav/pbs/abc.sh",shell=True);
                

def ConPara(fileName):
    tree=ET.parse(fileName);
    root=tree.getroot();

        #Reynolds number
    a=root[1][1][5].text;
    a=a.split('=');
    a=a[1];
    RE=float(a);

        #Final Time
    a=root[1][1][1].text;
    a=a.split('=');
    a=a[1];
    FT=float(a);

        #CheckSteps
    a=root[1][1][3].text;
    a=a.split('=');
    a=a[1];
    IO=float(a);

        #TimeStep]
    a=root[1][1][0].text;
    a=a.split('=');
    a=a[1];
    TS=float(a);
    ChkN=FT/(TS*IO);
    ChkN=int(ChkN);
    return FT, TS, IO, RE, ChkN;
    
def moveChk(CurrentPath,NewPath,ChkN):
    for files in glob(CurrentPath+'/*.chk'):
        a= os.path.basename(files);b=a.split('.')[0].split('_')[1];
        b=int(b)+ChkN;c='geom_'+str(b)+'.chk';os.rename(files,NewPath+'/'+c);
        
def ICFile(fileName,count,path1,path2):
    chkStr='geom_'+str(int(count))+'.chk';
    shutil.copy((path1+'/'+chkStr),path2);

    tree=ET.parse('1000.xml',OrderedXMLTreeBuilder());
    root=tree.getroot();
    root[1][6][0].set('FILE',chkStr);
    tree.write('1000.xml');

      
  
def sigma(path):
    fileList=[];x=[];y=[];
    for root, dirs, files in os.walk(path):
        for file in files:
            if (file.endswith(".mdl")):
                inE = os.path.join(root, file);
                fileList.append(inE);
    for f in fileList:
        case_str = f.split("/")
        case = Case();
        #case.alfa = Decimal(case_str[-5]);
        #case.mu = Decimal(case_str[-4]);                              
        #case.S = Decimal(case_str[-3]);
        case.Re = Decimal(float(case_str[-2]))
        #case.Name=str(case.alfa)+'_'+str(case.mu)+'_'+str(case.S)+'_'+str(case.Re);	 
        [pt,pr]=popt(f);
        print(pt[1]);print(case.Re);		
        case.popt=pt[1]/2.0;
        x.append(int(case.Re));
        y.append((pt[1]/2.0));
    print('the Reynolds number listi\n');
    print(x);
    print('the growth rate list \n');
    print(y);
    try:
        ReC=calcReC(x,y);
    except:
        print("the ReC is not defined for \t");
        ReC=-1;
    return x,y, ReC
            #return x,y;
        
    # ReC=calcReC(x,y);		#f=UnivariateSpline(x,y,s=0);
    #return x,y,ReC;

def ReSimulation(FilesPath,simPath,ReList,Beta,exe,filelist,itN):
    for R in ReList:
        os.chdir(simPath);
        if not os.path.exists(str(R)):
            os.makedirs(str(R));
        pathR =simPath+ '/' +str(R);
        os.chdir(pathR);
        shutil.copy((FilesPath+'/1000.xml'),pathR);
        shutil.copy((FilesPath+'/geom.xml'),pathR);
        shutil.copy((FilesPath+'/geomHplusD.fld'),pathR);
        [FT, TS, IO, RE, ChkN]= ConPara('1000.xml');
        tree=ET.parse('1000.xml',OrderedXMLTreeBuilder());
        root=tree.getroot();
        Re='Re='+str(R);
        root[1][1][5].text=Re;
        lz='LZ='+str((np.pi*2/(Beta)));
        root[1][1][8].text=lz
        tree.write('1000.xml');
        incSolver(exe,filelist);
        if(CheckEnergy('EnergyFile.mdl')):
            path2=pathR+'/2';
            if not os.path.exists(path2):            
                os.makedirs(path2);
            shutil.copy((pathR+'/1000.xml'),path2);
            shutil.copy((pathR+'/geom.xml'),path2);
        count=0;iter=1;
        while(CheckEnergy('EnergyFile.mdl')and iter<itN):
            os.chdir(path2);
            count=count+int(ChkN);
            ICFile('1000.xml',count,pathR,path2);
            incSolver(exe,filelist);	   
            subprocess.call(['sed "1,3d" EnergyFile.mdl > abc.txt'],shell=True);
            subprocess.call('cat ../EnergyFile.mdl abc.txt > ../abc.txt',shell=True);
            moveChk(path2,pathR,ChkN);
            iter=iter+1;
            os.chdir(pathR);
            os.rename('abc.txt','EnergyFile.mdl');
            shutil.rmtree('2/');   
    os.chdir(simPath); 
#if __name__ == '__main__':
#   f=sys.argv[1];
 #   ipVar(f)


def incSolver(exe,filelist):
    args=exe+'/IncNavierStokesSolver'+' '+filelist[0]+' '+filelist[1];
    print('Working in this directory \n');
    print(os.getcwd());
    subprocess.call(args,shell=True);

def incSolverP(exe,filelist):
    args=exe+' '+filelist[0]+' '+filelist[1]+' &';
    print('Working in this directory \n');
    print(os.getcwd());
    subprocess.call(args,shell=True); 

import numpy as np;
from case import *;
import extractdata;
from scipy.optimize import curve_fit;
def func(x, a, b):
    return a*np.exp(b*x);
    
def popt(file):
    case=Case();
    case.time,case.mod,case.energy = np.loadtxt(file, comments="\x00", skiprows=1, usecols=(0,1,2), unpack=True)
    up=1e-8;down=1e-18;
    if(case.time[0] > 100):N1=case.time[0]; case.time[0::2]=case.time[0::2]-N1;case.time[1::2]=case.time[1::2]-N1;
    case.t,case.e=extractdata.extractData(case,case.time[-1], up, down);
    print(case.t);
    popt, pcov = curve_fit(func, case.t, case.e, p0=(1e-15, 1e-2))
    perr = np.sqrt(np.diag(pcov))[0]+np.sqrt(np.diag(pcov))[1] ;
    print(popt[1]/2.0);
    return popt, perr;   

def calcReC(x,y):
    x.sort();y.sort();
    func=UnivariateSpline(x,y,k=3,s=0);
    for i in range(0,len(x)-1):
        temp=y[i+1];
        if((y[i] > 0 and temp <0) or (y[i]<0 and temp >0)):
            a=x[i]; b=x[i+1];
    tol=1e-6;
    while(abs(a-b)>tol):
        c=(a+b)/2.0;
        if(samesign(func,a,c)):b=c;
        else: a=c
    c=(a+b)/2.0;
    return c;

def samesign(func,a,b):
    c=func(a)*func(b);
    if(c<0):return 1;
    else: return 0;

def editGeo(pathS,pathD,a,S):
    path=pathS+'/'+'divConv2D.scr';      
    f=open(path,'r');
    d=f.readlines();
    d[3]='S='+str(S)+';\n';
    d[4]='a='+str(a)+';\n';
    f.close();
    path=pathD+'/'+'divConv2D.scr';
    f=open(path,'w');
    f.writelines(d);
    f.close();

def pbs(rse,name,module,wd,exe):
    f=open('pbs.sh','w');
    d=[];
    d.append('#!/bin/bash\n');
    d.append('#PBS -l '+rse+',walltime=05:00:00:00\n');
    d.append('#PBS -N '+name+'\n');
    d.append('#PBS -M nyadav@meil.pw.edu.pl\n');
    d.append('#PBS -m abe\n');
    d.append(module+'\n');
    d.append('cd '+wd+'\n');
    for i in exe:
        d.append(i+'\n');
    d.append('exit 0\n')
    f.writelines(d);
    f.close();

def nsvalues(path1):
    cwd=path1;
    path=glob('*/');
    x=[];y=[];
    for i in path:
        f=i.split('/')[0];
        newPath=cwd+'/'+f;
        print('the new path \n \n \n \n \n');
        print(newPath);
        print('\n \n \n \n \n \n');
        [a,b,c]=sigma(newPath);
        if(c > 0): 
            x.append(float(f));
            y.append(c);
    YX=zip(x,y);
    YX.sort();
    xx=[];yy=[];
    for i in range(0,len(YX)):
        yy.append(YX[i][0]);
        xx.append(YX[i][1]);

    return xx, yy;

def nsplot(Re ,beta):
    x=Re;y=beta;
    YX=zip(y,x);
    YX.sort();
    
    xx=[];yy=[];
    for i in range(0,len(YX)):
        yy.append(YX[i][0]);
        xx.append(YX[i][1]);
    fig, ax=plt.subplots();
    ax.plot(xx,yy);
    ax.grid(True);
    plt.ylabel('Beta');
    plt.xlabel('Reynolds Number');
    plt.show()



def nekFre(inE,obsPointNos,velDir):
    #skipRows number of points obspoints Number =+1 
    time=[]; fre=[];
    a=np.loadtxt(inE,skiprows=obsPointNos+1);
    x=a[:,0];
    y=a[:,velDir];
    f=interp1d(x,y,kind='cubic');

    xnew=np.linspace(x[0],x[-1],len(a[:,0])*100);
    ynew=f(xnew);

    for i in range(1,len(ynew)):
        if(np.sign(ynew[i-1])*np.sign(ynew[i]) < 0):
            time.append(xnew[i]);
    if(len(time)> 3 ):fre.append(time[3]-time[1]);
    return fre, time;

def poptEnRa(file,up=1e-8,down=1e-22):
    case=Case();
    case.time,case.mod,case.energy = np.loadtxt(file, comments="\x00", skiprows=1, usecols=(0,1,2), unpack=True)
    if(case.time[0] > 100):N1=case.time[0]; case.time[0::2]=case.time[0::2]-N1;case.time[1::2]=case.time[1::2]-N1;
    case.t,case.e=extractdata.extractData(case,case.time[-1], up, down);
    print(case.t);
    popt, pcov = curve_fit(func, case.t, case.e, p0=(1e-15, 1e-2))
    perr = np.sqrt(np.diag(pcov))[0]+np.sqrt(np.diag(pcov))[1] ;
    print(popt[1]/2.0);
    return popt, perr;   


def poptDir(path1):
    cwd=path1;
    path=glob('*/');
    x=[];y=[];
    for i in path:
        f=i.split('/')[0];
        newPath=cwd+'/'+f;
        os.chdir(newPath);
        print('working in this path \n \n \n \n \n');
        print(newPath);
        file=glob("*.mdl");
        file1=file[0];
        [a,b]=poptEnRa(file1,1e-8,1e-22);
        x.append(a[1]/2);
        y.append(float(f));
        os.chdir(cwd);
    if(len(x)==0):
        l1=x;
        l2=y;
    else:
        l2, l1 = zip(*sorted(zip(y, x)));
        l2=list(l2);l1=list(l1);
    return l1, l2;


def poptDirEn(path1,up,down):
    cwd=path1;
    path=glob('*/');
    x=[];y=[];
    for i in path:
        f=i.split('/')[0];
        newPath=cwd+'/'+f;
        os.chdir(newPath);
        print('working in this path \n \n \n \n \n');
        print(newPath);
        file=glob("*.mdl");
        file1=file[0];
        [a,b]=poptEnRa(file1,up,down);
        x.append(a[1]/2);
        y.append(float(f));
        os.chdir(cwd);
    #if(len(path==0):
    l2, l1 = zip(*sorted(zip(y, x)));
    l2=list(l2);l1=list(l1);
    return l1, l2;


