#!/bin/bash
#PBS -l nodes=1:tq2:ppn=1,walltime=05:00:00:00
#PBS -N 0.1_ts
#PBS -M nyadav@meil.pw.edu.pl
#PBS -m abe
/home/nyadav/anaconda2/bin/ipython2 manyObj.py 0.4  
exit 0

