import rf
import numpy as np

from rf.util import IterMultipleComponents
from rf import RFStream

import sys
import os

from hk_parameter import *

MDS=np.arange(30.0,90.1,1.0)
VPVSS=np.arange(1.5,2.01,0.01)



for station in stations:

    opath = "../output/"+station+"/" 
    os.system("mkdir -p "+ opath)
    
    
    st=rf.read_rf("../data/RF_"+station+".QHD")
    st.trim2(0, 90, 'onset')
    
    
    def iter3c(stream):
        return IterMultipleComponents(stream, key='onset', number_components=(2, 3))
    
    
    for cnt, st3c in enumerate(iter3c(st)):
    
        print("processing",station,"event no.", cnt, "/", len(iter3c(st)))
    
        stream3c=RFStream()
        stream3c.append(st3c[0])
        stream3c.append(st3c[1])
        stream3c.append(st3c[2])
    
        try:
            trl=stream3c.select(component="L")[0]
            trq=stream3c.select(component="Q")[0]
    
            lmax=np.abs(trl.data).max()
            qmax=np.abs(trq.data).max()
        except:
            print("component L or Q do not exist for event")
            continue
    
        slow=round(trl.stats.sh.SLOWNESS,2)
        slow=slow/111.2
    
        # initiaization
        if cnt==0:
    
            timesgrid_ps=np.zeros([MDS.size, VPVSS.size])
            timesgrid_ppps=np.zeros([MDS.size, VPVSS.size])
            timesgrid_ppss=np.zeros([MDS.size, VPVSS.size])
    
            HK_STACK      = np.zeros([MDS.size, VPVSS.size])
            HK_STACK_PS   = np.zeros([MDS.size, VPVSS.size])
            HK_STACK_PPPS = np.zeros([MDS.size, VPVSS.size])
            HK_STACK_PPSS = np.zeros([MDS.size, VPVSS.size])
    
        if lmax<0.00001 or qmax<0.00001:
            print("either l or q has no data")
            continue
    
    
        times=trq.times()
        qrfdata=trq.data
    
        for i,MD in enumerate(MDS):
            for j,VPVS in enumerate(VPVSS):
            
    
                vs=vp/VPVS
                termp=1/(vp**2)-slow**2
                terms=1/(vs**2)-slow**2
    
                #if 
    
                if termp < 0 :
                    print("over critical angle",slow,vp,termp,", --- abort.")
                    continue  
    
                PS   =     MD * (np.sqrt(terms)-np.sqrt(termp))
                PPPS =     MD * (np.sqrt(terms)+np.sqrt(termp))
                PPSS = 2 * MD *  np.sqrt(terms)
    
                timesgrid_ps[i,j]=PS
                timesgrid_ppps[i,j]=PPPS
                timesgrid_ppss[i,j]=PPSS
    
    
    
        tmp_HK_STACK_PS   = np.interp(timesgrid_ps  ,times,qrfdata) * w_ps
        tmp_HK_STACK_PPPS = np.interp(timesgrid_ppps,times,qrfdata) * w_ppps
        tmp_HK_STACK_PPSS = np.interp(timesgrid_ppss,times,qrfdata) * w_ppss * (-1)
    
        tmp_HK_STACK = tmp_HK_STACK_PS + tmp_HK_STACK_PPPS + tmp_HK_STACK_PPSS
    
    #    tmp_HK_STACK      /= tmp_HK_STACK.max()
    #    tmp_HK_STACK_PS   /= tmp_HK_STACK_PS.max()
    #    tmp_HK_STACK_PPPS /= tmp_HK_STACK_PPPS.max()
    #    tmp_HK_STACK_PPSS /= tmp_HK_STACK_PPSS.max()
    
        HK_STACK_PS   += tmp_HK_STACK_PS
        HK_STACK_PPPS += tmp_HK_STACK_PPPS
        HK_STACK_PPSS += tmp_HK_STACK_PPSS
    
        HK_STACK      += tmp_HK_STACK


    output="NPY"

    if output=="NPY":    
        
        np.save(opath + "HK_ALL.npy"   , HK_STACK)
        np.save(opath + "HK_PS.npy"    , HK_STACK_PS)
        np.save(opath + "HK_PPPS.npy"  , HK_STACK_PPPS)
        np.save(opath + "HK_PPSS.npy"  , HK_STACK_PPSS)
        np.save(opath + "HK_MDS.npy"   , MDS)
        np.save(opath + "HK_VPVSS.npy" , VPVSS)
    
    if output=="TXT":
        
        phaselist=["PPSS","PPPS","PS","ALL"]
        for STACKS in [HK_STACK, HK_STACK_PS,  HK_STACK_PPPS, HK_STACK_PPSS]:
    
            label=phaselist.pop()
            ofile=opath + "STACK_" + label + ".txt"
            fo=open(ofile, "w")
            for i,MD in enumerate(MDS):
                 for j,VPVS in enumerate(VPVSS):
                     print(VPVS,MD, STACKS[i,j], file = fo)
     
            
    
