import ipVar, funcs, os;
from output import *;
from decimal import Decimal;
import numpy as np;

out=Output();
cwd=os.getcwd();
for root, dir, files in os.walk("./"):
    for file in files:
        if(file.endswith(".his")):
            print(root);
            inE=os.path.join(root,file);
            out.Re.append(Decimal(root.split('/')[-1]));
            out.beta.append(Decimal(root.split('/')[-2]));
            #out.alpha.append(Decimal(root.split('/')[-4]));
            out.alpha.append(Decimal(1));
            case=Case();
            os.chdir(root);
            enrFile=glob('*.mdl');
            print(inE);
            if (len(enrFile)> 0):
                enrFile1=enrFile[0];
                [popt, perr]=ipVar.poptEnRa(enrFile1,1e-8,1e-21);
                out.sigma.append(popt[1]/2.0);
                case.time,case.mod,case.energy = np.loadtxt(enrFile1, comments="\x00", skiprows=1, usecols=(0,1,2), unpack=True);
                t, e=extractdata.extractData(case,case.time[-1], 1e-8, 1e-21);
           
            inE=glob('*.his');inE=inE[0];
            [a, b]=ipVar.nekFre3(inE,1,3,-1);
            out.sigmaR.append(a);   
            os.chdir(cwd);
            
n=len(out.Re);
x=np.zeros((n,5),dtype=np.float);
x[:,0]=out.alpha[:];
x[:,1]=out.beta[:];
x[:,2]=out.Re[:];
x[:,3]=out.sigma[:];
x[:,4]=out.sigmaR[:];
np.savetxt('out.csv',x,delimiter=" ");



