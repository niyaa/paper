import sys, os, subprocess;

sys.path.append("~/Dropbox/script")
import funcs;

def dist():
    N=funcs.MaxChk(os.getcwd());

    for i in range(0,N+1):
        args='FldAddFld -1 1 geom3D.bse  geom_'+str(i)+'.chk '+'geom'+str(i)+'.fld';
        subprocess.call(args,shell=True);
        args='FldToVtk geom'+str(i)+'.fld geom.xml';
        subprocess.call(args,shell=True);


def vtu():
    path=os.getcwd();
    N=funcs.MaxChk(path);
    for i in range(0,N+1):
        args='FieldConvert geom.xml '+'geom_'+str(i)+'.chk '+'geom_'+str(i)+'.vtu';
        subprocess.call(args,shell=True);
