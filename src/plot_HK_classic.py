import pylab as plt
import numpy as np
import os

from hk_parameter import *

for station in stations:
    
    
    opath = "../output/"+station+"/" 
    rpath = "../results/"+station+"/" 
    os.system("mkdir -p "+ rpath)
    
    
    
    HK_STACK  = np.load(opath + "HK_ALL.npy")
    HK_STACK1 = np.load(opath + "HK_PS.npy")
    HK_STACK2 = np.load(opath + "HK_PPPS.npy")
    HK_STACK3 = np.load(opath + "HK_PPSS.npy")
    MDS       = np.load(opath + "HK_MDS.npy")
    VPVSS     = np.load(opath + "HK_VPVSS.npy")
    
    
    # restrict search range 

    vpvs_min=search_range_dict[station]['vpvs_min']
    vpvs_max=search_range_dict[station]['vpvs_max']
    Moho_min=search_range_dict[station]['Moho_min']
    Moho_max=search_range_dict[station]['Moho_max']



    vpvsrange = (VPVSS > vpvs_min) * (VPVSS < vpvs_max)
    MDrange   = (MDS   > Moho_min) * (MDS   < Moho_max)
    
    maxpos=np.where(HK_STACK[MDrange,:][:,vpvsrange]==HK_STACK[MDrange,:][:,vpvsrange].max())
    
    best_vpvs=VPVSS[vpvsrange][maxpos[1]][0]
    best_md=MDS[MDrange][maxpos[0]][0]
    
    
    
    fig=plt.figure(figsize=(8.4,4))
    ax1=fig.add_subplot(121)
    ax2=fig.add_subplot(122)
    
    ax1.set_title(station)
    ax1.pcolor(VPVSS, MDS, HK_STACK)
    ax1.set_ylim(MDS[0],MDS[-1])
    ax1.set_xlim(VPVSS[0],VPVSS[-1])
    
    ax2.set_title("")
    
    
    coppps=0.6
    coppss=0.5
    cops=0.6
    
    
    
    maps=HK_STACK1[MDrange,:][:,vpvsrange].max()
    mappps=HK_STACK2[MDrange,:][:,vpvsrange].max()
    mappss=HK_STACK3[MDrange,:][:,vpvsrange].max()
    
    ax2.contourf(VPVSS, MDS, HK_STACK1,np.arange(cops,1.05,0.05)   * maps, cmap="Blues" , vmin=0., vmax=maps, zorder=0.1, extend="max")
    ax2.contourf(VPVSS, MDS, HK_STACK2,np.arange(coppps,1.05,0.05) * mappps, cmap="Greens" , vmin=0., vmax=mappps, zorder=0.2, extend="max")
    ax2.contourf(VPVSS, MDS, HK_STACK3,np.arange(coppss,1.05,0.05) * mappss, cmap="Reds" , vmin=0., vmax=mappss, zorder=0.3, extend="max")
    
    
    
    for ax in [ax1, ax2,]:
        ax.plot([best_vpvs,best_vpvs],[MDS[0],best_md], "k-")
        ax.plot([VPVSS[0],best_vpvs],[best_md,best_md], "k-")
        ax.plot([best_vpvs],[best_md], "wo", markeredgecolor = "black")
    
        ax.set_ylim(MDS[0],MDS[-1])
        ax.set_xlim(VPVSS[0],VPVSS[-1])
    
        ax1.set_ylabel("Moho Depth (km)")
        ax.set_xlabel("Vp/Vs")
    
    plt.savefig(rpath + "HK_classic.png")
    
    f=open(rpath + "best_values_HK_classic","w")
    print( "best_vpvs = ", best_vpvs, "best_MohoDepth = ", best_md, station, "MAXVAL = ", HK_STACK.max(), file=f)
    
    f.close()
    

