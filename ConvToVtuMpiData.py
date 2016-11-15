import sys;
sys.path.append('/home/nyadav/pyscr/');
import nekOpr;
import os;
from glob import glob;
cwd=os.getcwd();
path=['0.675']

for i in path:
    os.chdir(i);
    try:
        nekOpr.vtu();
    except:
        print("there is no vtu file \n");
    
    pathNew=os.getcwd();
    path1=glob("*/");
    for i in path1:
        os.chdir(i);
        try:
            nekOpr.vtu();
        except:
            print("There is no vtu file \n");
        os.chdir(pathNew);
    os.chdir(cwd);
