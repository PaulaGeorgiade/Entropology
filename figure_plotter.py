from utilities import read_df, run_gamma_error , run_gamma 
from diversity_calculators import calc_similarity, calc_diversity
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import itertools
plt.rcParams.update({'font.size': 30, "font.family":"helvetica"})
from matplotlib.offsetbox import AnchoredText
from collections import defaultdict
import networkx as nx

if __name__ == "__main__":
    
    ##############
    # Load database & plot (FIGURE 2 MAIN TEXT)
    ##############
    dbname = "NoEarlyDates_WorkingDB_Modelled" 
    pcol = "Solo_Period"
    db = read_df(exclude_periods = ["LM", "LM III", "LM III A", "LM III B"], dbname = dbname, pcol = pcol, map_periods = True)
    
    
    ##############
    # Gamma diversity with errorbars (FIGURE 5, FIGURE 3(b) MAIN TEXT) 
    ##############
    run_gamma_error(db,0.1,dbname =dbname, pcol= pcol, figname= "Fig5.eps") # 
    run_gamma(db,dbname =dbname, pcol= pcol,figname= "Fig3.eps")
    
    sites =sorted(list(set(db.Deposition_Site)))
    periods= sorted(list(set(db[pcol])))
    
    ##############
    # Inter-period similarity (TABLE 2 MAIN TEXT)
    ##############
    D={}
    eff = False
    for p in sorted(set(db.Solo_Period)):
        samples = []
        for s in sites:
            samples.append(list(db[(db[pcol] ==p) & (db.Deposition_Site==s)]["Vessel_Form"]))
        D[p]= samples
    for i in range(len(periods)-1):
        p1,p2 = periods[i], periods[i+1]
        s1,s2 = [], []
        for s in D[p1]:
            s1+=s
        for s in D[p2]:
            s2+=s
    eff = True # if use effective or landscape aggregation 
    intra_period_similarity = {}
    for i in range(len(periods)-1):
        p1,p2 = periods[i], periods[i+1]
        print(p1,p2,end=" ")
        for q in [0,.5,1,2]:
            res = []
            for sample in D[p1]:
                for sample2 in D[p2]:
                    if len(sample)!=0 and len(sample2)!=0:
                        if q== 2:
                            res.append(calc_similarity([sample,sample2],q, True))
                        else:
                            
                            res.append(calc_similarity([sample,sample2],q, eff))
                    else:
                        res.append(0)
            print(round(np.mean(res),2)," ",round(np.std(res),2),  end=",")
            
    ###################
    # Table replacement
    ###################
    graph_list =[[0, 'LM II', 'LM III A1', 0.36850323937820184],
     [0.5, 'LM II', 'LM III A1', 0.5169973358901473],
     [1, 'LM II', 'LM III A1', 0.6350543067014085],
     [2, 'LM II', 'LM III A1', 0.724621225495097],
     [0, 'LM III A1', 'LM III A2', 0.45574130461363005],
     [0.5, 'LM III A1', 'LM III A2', 0.5829699755694543],
     [1, 'LM III A1', 'LM III A2', 0.6728201724055703],
     [2, 'LM III A1', 'LM III A2', 0.7267556766980137],
     [0, 'LM III A2', 'LM III B1', 0.2159211219447572],
     [0.5, 'LM III A2', 'LM III B1', 0.3182786126849091],
     [1, 'LM III A2', 'LM III B1', 0.41304593443751564],
     [2, 'LM III A2', 'LM III B1', 0.45089638901740403],
     [0, 'LM III B1', 'LM III B2', 0.059867024587612824],
     [0.5, 'LM III B1', 'LM III B2', 0.09993757112406364],
     [1, 'LM III B1', 'LM III B2', 0.13627016466505842],
     [2, 'LM III B1', 'LM III B2', 0.14712327905128134]]


    vnames = ['LM II' , 'LM III A1' , 'LM III A2', 'LM III B1', 'LM III B2']
    q_color = {0: "tab:blue", 0.5: "tab:orange", 1: "tab:purple", 2:"tab:red" }
    options = {"edgecolors": "tab:gray", "node_size": 800, "alpha": 1}
    pos = {'LM II':  np.array([-1,-1]) , 
     'LM III A1': np.array([-0.5,-0.5]) , 
     'LM III A2': np.array([0, 0]),
     'LM III B1': np.array([0.5, 0.5]),
     'LM III B2': np.array([1,1])}

    fig,ax = plt.subplots(1,4,figsize =(19,5))
    i = 0
    for q in [0,0.5,1,2]:
        g = nx.Graph()
        widths = []
        for item in graph_list: 
            if item[0] == q:    
                g.add_edge(item[1] , item[2], weight = item[-1])
                widths.append( item[-1] * 10/0.724621225495097)
                
        nx.draw_networkx_nodes(g, pos, nodelist=vnames, node_color=q_color[q], ax = ax[i], **options)
        nx.draw_networkx_edges(g,pos, width=widths , alpha=0.5, edge_color=q_color[q],ax = ax[i] )
        nx.draw_networkx_labels(g, pos=pos,ax = ax[i],
                                labels=dict(zip(vnames,vnames)),
                                font_color='black',font_size=20)
        # ax[i].box(False)

        at = AnchoredText(
            f"q={q}", prop=dict(size=20), frameon=False, loc='upper left')
        # at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
        ax[i].add_artist(at)
        ax[i].spines['top'].set_visible(False)
        ax[i].spines['right'].set_visible(False)
        ax[i].spines['bottom'].set_visible(False)
        ax[i].spines['left'].set_visible(False)
        ax[i].set_ylim(-1.35,1.35)
        ax[i].set_xlim(-1.35,1.35)
        i +=1
    plt.tight_layout()
    plt.savefig(f"inter_period_similarity.svg")
    plt.show()
            
            
    ###################
    # Size vs diversity (FIGURE 4 MAIN TEXT)
    ###################
    fig,ax = plt.subplots(1,1,figsize=(15,8))
    i =0
    q=1
    c=0
    markers = ["o","^","*","s","v"]
    site_diversity_vs_size = []
    for site,df in db.groupby("Deposition_Site"):
        y = []
        x = []
        print(site)
        for date, X in df.groupby(pcol):
                print(date,end =",")
                c+=1
                y.append(calc_diversity(X.Vessel_Form,q))
                x.append(len(X))
        ax.plot(x,y,label = site,linestyle = "",marker = markers[i],markersize =20,linewidth = 5 )
        i+=1
    plt.xlabel("$N$")
    plt.ylabel("$D_1$", fontsize=40)
    ax.set_xscale("symlog")
    ax.set_xticks([1, 10, 100, 1000])
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.set_ylim(-0.1,20)
    ax.set_xlim(0,3000)
    ax.legend(loc='center left',fancybox=False,bbox_to_anchor=(1, 0.5), shadow=False,ncol=1)
    plt.tight_layout()
    plt.savefig(f"./figures/{dbname}/{pcol}/Fig4.eps")
    plt.show()
     
    
    ###################
    # Similarity within period (FIGURE 6 MAIN TEXT)
    ###################
    fig,ax = plt.subplots(1,2,figsize =(22,9))
    for q in [0,2]:
        if q==0 : i = 1 
        else :i = 0
        eff=  True
        D  = defaultdict(list)
        if q == 0: 
            at = AnchoredText(
                "(b)", prop=dict(size=35), frameon=False, loc='upper left')
            # at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
            ax[i].add_artist(at)
        else:
            
            at = AnchoredText(
                "(a)", prop=dict(size=35), frameon=False, loc='upper left')
            # at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
            ax[i].add_artist(at)
          
          
        for p ,df in db.groupby(pcol):
            for site,set1 in df.groupby("Deposition_Site"):
                D[(site,p)] = list(set1.Vessel_Form)
        G = {}
        min_val=0
        for n1 ,n2  in itertools.combinations(D.keys(),2):
            G[(n1,n2)] = calc_similarity([D[n1],D[n2]],q,effective = eff)
        
        site_sim_in_period =defaultdict(list)
        for s1 in sites:
            for p in periods:
                val = []
                sample1 = list(db[(db[pcol]==p) & (db.Deposition_Site==s1)].Vessel_Form)
                if len(sample1) >0:
                    for s2 in [s for s in sites if s!= s1]:
                        sample2 = list(db[(db[pcol]==p) & (db.Deposition_Site==s2)].Vessel_Form)
                        if len(sample2) > 0: 
                            val.append(calc_similarity([sample1,sample2],q,effective = eff))
                        else: 
                            val.append(0) 
                else:
                    val = [0 for i in range(4)]
                site_sim_in_period[s1].append(np.mean(val))
                
        markers = ["o","^","*","s","v"]
        for key,val in site_sim_in_period.items():
            if i ==0:
                ax[i].plot(periods,val,linestyle ="-", marker= markers.pop(),markersize=20,label=key)
                
            else:
                ax[i].plot(periods,val,linestyle ="-", marker= markers.pop(),markersize=20)
        ax[i].set_ylim(-0.1,1)
        if q==1:
            ax[i].set_ylabel("$\\langle S_1(A,B)\\rangle_B$", fontsize = 35)
        if q==2:
            ax[i].set_ylabel("$\\langle S_2(A,B)\\rangle_B$", fontsize = 35)
        if q==0:
            ax[i].set_ylabel("$\\langle S_0(A,B)\\rangle_B$", fontsize = 35)
        fig.legend(loc='upper center',fancybox=False,bbox_to_anchor=(0.5,0), shadow=False,ncol=5,title = "A")
        plt.tight_layout()
        plt.savefig(f"./figures/{dbname}/{pcol}/Fig6.eps", bbox_inches = "tight")
        

    ###################
    # Shuffled diversity vs observed
    ###################
    # fig, ax = plt.subplots(1,1,figsize=(15,8))
    # q=1
    # for frac in np.linspace(0.1,1,4):#[0.1,0.3,0.6,1]:
    #     color= {"Chania":"blue","Knossos":"orange","Kommos":"green","Mochlos":"red", "Palaikastro":"purple"}
    #     markers = {"Chania":"o","Knossos":"v","Mochlos":"s","Kommos":"*","Palaikastro":"^"}
    #     for site in sites:
    #         site_res = []
    #         site_size =[]
    #         for p in sorted(set(db[pcol])):
    #             sample = list(db[db[pcol]==p][db.Deposition_Site == site].Vessel_Form)
    #             if len(sample)!=0:
    #                 samples_shuffled = []
    #                 for r in range(100):
    #                     shuffled = random_replacement(db, sample,frac,uniform=True)
    #                     samples_shuffled.append(calc_diversity(shuffled,q))
    #                 site_size.append(len(sample))
    #                 site_res.append(np.mean(samples_shuffled) - calc_diversity( sample,q))
    #         if frac ==1:
    #             ax.plot(site_size, site_res, marker =markers[site] , markersize = 20,label = site,linestyle="",alpha=frac,color=color[site])
    #         else:
    #             ax.plot(site_size, site_res, marker =markers[site] , markersize = 20,linestyle="",alpha=frac,color=color[site])
         
    # ax.legend(loc='center left',fancybox=False,bbox_to_anchor=(1, 0.5), shadow=False,ncol=1)
    # ax.set_xscale("symlog")
    # ax.set_xticks([1, 10, 100,1000])
    # ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    # ax.set_xlabel("$N$")
    # ax.set_ylabel("$\\langle D _1^{\\mathrm{shuffled}}\\rangle- D_1$")
    # plt.tight_layout()
    # plt.savefig(f"./figures/{dbname}/{pcol}/Fig6.svg")
    # plt.show()
      
    # ###################
    # # Similarity within period
    # ###################
    # fig,ax = plt.subplots(1,1,figsize=(10,10))
    # markers = ["o","^","*","s","v"]
    # colors = ["orange","green"]
    # for q in [0.5, 1]:
    #     sim = []
    #     for p in periods:
    #         print(p)
    #         samples = [list(group["Vessel_Form"]) for s,group in db[db.Solo_Period ==p].groupby("Deposition_Site")]
    #         while len(samples ) < 5:
    #             samples.append([])
    #         sim.append( calc_similarity(samples, q=q, effective= False ))
    #     ax.plot(periods, sim,label = "$q=$"+str(q),linestyle = "--",markersize =20,marker = markers.pop(0), linewidth = 1 ,color = colors.pop(0))
    
    # ax.legend(loc='center left',fancybox=True,bbox_to_anchor=(1, 0.5), shadow=True,ncol=1)
    # ax.tick_params(axis ="x" ,rotation = 90)
    # plt.tight_layout()
    # plt.savefig("similarity_within_period.pdf")
    # plt.savefig("similarity_within_period.svg")

    # ###################
    # # Similarity network
    # ###################
    # import networkx as nx
    # g = nx.Graph()
    # for p in periods:
    #     for s in sites:
    #         g.add_node((s,p))
    # for key,val in G.items():
    #     g.add_edge(key[0],key[1],weight = val)
    
    # ypos = {"Chania": 1, "Knossos": 2, "Kommos":3, "Mochlos":4, "Palaikastro":5 }
    # xpos = {"LM II": 1, "LM III A1": 2, "LM III A2" : 3, "LM III B1": 4, "LM III B2": 5}
    # pos = {}
    # for n in g.nodes():
    #     pos[n] = (ypos[n[0]],xpos[n[1]])
    # fig,ax =plt.subplots(figsize=(10,10))
    # nx.draw_networkx_edges(g, pos, edgelist = list(G.keys()), width = list(G.values()),ax=ax)
    # nx.draw_networkx_nodes(g, pos,nodelist = list((dict(g.degree(weight="weight")).keys())),node_color="k", node_size = list(40*np.array(list(dict(g.degree(weight="weight")).values()))),ax=ax)
    # ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    # ax.set_yticks(np.arange(1, 6, 1))
    # ax.set_xticks(np.arange(1, 6, 1))
    # ax.set_yticklabels(list(ypos.keys()),fontsize= 20)
    # ax.set_xticklabels(list(xpos.keys()),fontsize= 20)
    # plt.tight_layout()
    # fig.savefig("graph.svg")

    # ###################
    # # Site diversity
    # ###################
    # site_diversity = {}
    # for site,df in db.groupby("Deposition_Site"):
    #     print(site)
    #     y = []
    #     for p in periods:
    #         print(p,end =",")
    #         X = df[df.Solo_Period==p].Vessel_Form
    #         if len(X)!=0: 
    #             y.append(calc_diversity(df[df.Solo_Period==p].Vessel_Form,q))
    #         else: 
    #             y.append(0)
    #     site_diversity[site] = y
    # markers = ["o","^","*","s","v"]
    # fig,ax = plt.subplots(1,1,figsize =(15,8))
    # for site in sites:
    #     ax.scatter(site_diversity[site], site_sim_in_period[site],marker = markers.pop(0),s=300,label=site)
    # ax.set_ylabel("$\\langle S_q(A,B)\\rangle_B$", fontsize = 35)
    # ax.set_xlabel("$D_q(A)$", fontsize = 35)
    # plt.title(f"Similarity vs Diversity, q={q}")
    # ax.legend(loc='center left',fancybox=True,bbox_to_anchor=(1, 0.5), shadow=True,ncol=1, title = "A")
    # plt.tight_layout()
    # plt.savefig(f"./figures/figs/in_period_similarity_vs_diversity_effective_{eff}_q_{q}.pdf")
    # plt.savefig(f"./figures/figs/in_period_similarity_vs_diversity_effective_{eff}_q_{q}.svg")
    
    
    
    
            
