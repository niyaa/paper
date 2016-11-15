import sys;
sys.path.append('/home/llaniewski/TP/build/lib')
sys.path.append('/home/llaniewski/TP/build/lib/site-packages')

sys.path.append('/home/nyadav/anaconda2/lib/python2.7/site-packages')
from paraview.simple import *;
from paraview.numeric import fromvtkarray;
from scipy import interpolate, optimize, integrate;
import math;
from glob import glob;
import os;
import numpy as np;
t=int(raw_input("Enter time step \n"));

vtuN=glob("*.vtu");
N=len(vtuN);
Qx=[];
Qy=[];
Qz=[];

for i in range(0,N):
    inE=os.getcwd()+'/geom_'+str(i)+'.vtu';
    geomvtu = XMLUnstructuredGridReader(FileName=[inE])
    geomvtu.PointArrayStatus = ['u', 'v', 'w', 'p']
    slice1=Slice(Input=geomvtu)
    slice1.SliceType='Plane';
    slice1.SliceOffsetValues = [0.0];
    xslice = math.pi / 0.5
    slice1.SliceType.Origin = [xslice, 0.0, 0.0];
    slice1.SliceType.Normal=[0,0,-1]
    slice1.SliceOffsetValues = [0.0]
    slice1.UpdatePipeline();
    pl = servermanager.Fetch(slice1)
    nbp = pl.GetNumberOfPoints()
    pos1 = fromvtkarray(pl.GetPoints().GetData())
    integrateVariables1 = IntegrateVariables(Input=slice1);
    Q=integrateVariables1.PointData[3]
    qz=Q.GetRange()[0];
    Qz.append(qz);
    Q=integrateVariables1.PointData[2]
    qy=Q.GetRange()[0];
    Qy.append(qy);
    Q=integrateVariables1.PointData[1];
    qx=Q.GetRange()[0];
    Qx.append(qx);

a=np.zeros((len(Qz),4),dtype=np.float);
for i in range(0,len(Qz)):
    a[i,0]=t*i;
Qp=2*np.pi*4/3.0;
for i in range(0,len(Qz)):
    a[i,3]=Qz[i]/Qp;
    a[i,2]=Qy[i];
    a[i,1]=Qx[i];
np.savetxt('SatFr.txt',a);
