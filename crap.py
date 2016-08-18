import subprocess;
import os;
from glob import glob;

print(os.getcwd());
subprocess.call('ls -al',shell=True);

def funC():
    path=glob('*/');
    if(len(path)>0):
        return len(path)
    if(len(path)==0):
        return(os.getcwd());


def funA():
    print('This is function A \n ');

def funB():
    print('This is the function B \n');


def funD(a):
    if(a==0):
        print('a is zero\n');
    if(a>1):
        print('a is not zero \n');

