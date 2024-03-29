from utilities import read_df, run_gamma_error , run_gamma , run_beta
from diversity_calculators import calc_similarity, calc_diversity
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import itertools
plt.rcParams.update({'font.size': 30, "font.family":"helvetica"})
from matplotlib.offsetbox import AnchoredText
from collections import defaultdict
import networkx as nx
import matplotlib as mpl
from mycolorpy import colorlist as mcp
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

if __name__ == "__main__":
    
    ##############
    # Load database & plot (FIGURE 2 MAIN TEXT)
    ##############
    # dbname = "STANDARD_DATES_SettlementTomb_new2022" 
    # pcol = "New Merged Dates"
    # map_periods = False
    dbname= "Entropology_Dataset_Flattened"
    pcol = "Solo_Period"
    map_periods = True
    db = read_df(exclude_periods = ["LM", "LM III", "LM III A", "LM III B"], dbname = dbname, pcol = pcol, map_periods = map_periods)
    
    

    colors = mcp.gen_color(cmap="viridis",n=5)
    sites=  ["Chania", "Kommos", "Knossos", "Mochlos", "Palaikastro"]
    site_colors= dict(zip( sites, colors))
    ###############
    # FIGURE 2 MAIN TEXT
    ###############
    h_site_tot = {}
    for site, group in db.groupby("Deposition_Site"):
        h_site_tot[site] = len(group)
    # color= {"Chania":"tab:blue","Knossos":"tab:orange","Kommos":"tab:green","Mochlos":"tab:red", "Palaikastro":"tab:purple"}
    h={}
    hatch_styles = {"Chania": "/","Kommos": "X", "Knossos": "+", "Mochlos": "\\", "Palaikastro": "."}
    for key,val in db.groupby("Vessel_Form"):
        h[key] = len(val)
    h = {k:v for k,v in sorted(h.items(), key = lambda item: item[1], reverse =True)}
    h_site={}
    for site in set(db.Deposition_Site):
        arr = []
        for key in h.keys():
            arr.append(len(db[(db.Vessel_Form == key) & (db.Deposition_Site == site)]))
            h_site[site] = arr
    fig,ax = plt.subplots(1,1,figsize=(22,10))
    ax.yaxis.grid(True,which='major')
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    axi = inset_axes(ax, width = 4, height = 3)
    # axi.set_ylim(0,1)
    
    axi.yaxis.grid(True,which='major')
    bottom_values = [0 for i in range(len(set(db.Vessel_Form)))]
    for site in ["Mochlos", "Palaikastro", "Knossos", "Kommos", "Chania" ]:
        ax.bar(list(h.keys()), h_site[site],bottom = bottom_values,width=0.7, 
               alpha = 1, label = site, color = site_colors[site])#,hatch = hatch_styles[site] +hatch_styles[site])
        bottom_values =np.add(bottom_values,  h_site[site])
    for site in ["Chania", "Kommos", "Knossos", "Palaikastro", "Mochlos" ]:
        axi.bar(site, h_site_tot[site], color = site_colors[site])#, hatch = hatch_styles[site])
    plt.xticks(rotation=90)
    ax.tick_params(axis = "y", length = 10, width=2  , which = "both")
    ax.tick_params(axis='x', labelrotation = 90)
    ax.set_yscale('symlog')
    axi.set_yscale("symlog")
    axi.set_yticks([1, 10, 100, 1000, 10000])
    ax.set_yticks([0, 1, 10, 100, 1000])
    ax.set_ylim(0,3000)
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    plt.tight_layout()
    plt.savefig(f"./figures/{dbname}/{pcol}/Fig2.eps")
    plt.savefig(f"./figures/{dbname}/{pcol}/Fig2.pdf")
    plt.savefig(f"./figures/{dbname}/{pcol}/Fig2.svg")
    plt.savefig(f"./figures/{dbname}/{pcol}/Fig2.png")

    
    
    ##############
    # Gamma diversity with errorbars (FIGURE 5, FIGURE 3(b) MAIN TEXT) 
    ##############
    run_gamma_error(db,0.1,dbname =dbname, pcol= pcol, figname= "Fig5", ylimit = 45, cmapname ="viridis") # 
    run_gamma(db,dbname =dbname, pcol= pcol,figname= "Fig3")
    
    sites =sorted(list(set(db.Deposition_Site)))
    periods= sorted(list(set(db[pcol])))
    
    
    
    ###################
    # Beta diversity
    ###################
    run_beta(db,dbname =dbname, pcol= pcol)
    

    

    
    ##############
    # Inter-period similarity (TABLE 2 MAIN TEXT)
    ##############
    D={}
    eff = False
    for p in sorted(set(db[pcol])):
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
    graph_list = []
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
            graph_list.append([q, p1, p2, np.mean(res)])
        print('')
    
            
    ###################
    # Size vs diversity (FIGURE 4 MAIN TEXT)
    ###################
    fig,ax = plt.subplots(1,1,figsize=(15,8))
    ax.xaxis.grid(True,which='major')
    ax.yaxis.grid(True,which='major')
    ax.set_yticks(np.linspace(0,20, 11))
    q=1
    markers = ["o","^","s","v", "*"]
    period_markers = dict(zip(sorted(list(set(db.Solo_Period))),markers))
    legend_elements = [Patch(facecolor=site_colors[site],edgecolor = site_colors[site],label= site) for site in sites] + [Line2D([0], [0], marker=period_markers[period], color='w', label=period, markerfacecolor='w',markeredgecolor="k", markersize=15) for period in period_markers.keys()]
    site_diversity_vs_size = []
    for site in sites:
        df =db[db.Deposition_Site == site]
        y = []
        x = []
        print(site)
        for date, X in df.groupby(pcol):
            print(date,end =",")
            y.append(calc_diversity(X.Vessel_Form,q))
            x.append(len(X))
            ax.scatter(len(X), calc_diversity(X.Vessel_Form,q), marker = period_markers[date], s= 300,color = site_colors[site])
        # ax.plot(x,y,label = site,linestyle = "",marker = markers[i],markersize =20 ,color = site_colors[site])
        # i+=1
    plt.xlabel("$N$")
    plt.ylabel("$D_1$", fontsize=40)
    ax.set_xscale("symlog")
    ax.set_xticks([1, 10, 100, 1000])
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.set_ylim(0,20)
    ax.set_xlim(0,3000)
    ax.legend(handles = legend_elements, loc='center left',fancybox=False,bbox_to_anchor=(1, 0.5), shadow=False,ncol=1)
    plt.tight_layout()
    plt.savefig(f"./figures/{dbname}/{pcol}/Fig4.eps")
    plt.savefig(f"./figures/{dbname}/{pcol}/Fig4.pdf")
    plt.savefig(f"./figures/{dbname}/{pcol}/Fig4.svg")
    plt.savefig(f"./figures/{dbname}/{pcol}/Fig4.png")
    plt.show()
     
    
    ###################
    # Similarity within period (FIGURE 6 MAIN TEXT)
    ###################
    fig,ax = plt.subplots(1,2,figsize =(22,9))
    ax[1].yaxis.grid(True,which='major')
    ax[0].yaxis.grid(True,which='major')
    for q in [0,2]:
        if q==0 : i = 1 
        else :i = 0
        eff=  True
        D  = defaultdict(list)
        if q == 0: 
            at = AnchoredText(
                "(b)", prop=dict(size=35), frameon=False, loc='upper left')
            ax[i].add_artist(at)
        else:
            
            at = AnchoredText(
                "(a)", prop=dict(size=35), frameon=False, loc='upper left')
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
        markers = ["o","o","o","o","o"]
        for key,val in site_sim_in_period.items():
            if i ==0:
                ax[i].plot(periods,val,linestyle ="-", marker= markers.pop(),markersize=15,label=key ,markerfacecolor = site_colors[key], markeredgewidth =3,color = site_colors[key])
                
            else:
                ax[i].plot(periods,val,linestyle ="-", marker= markers.pop(),markersize=15,markerfacecolor =site_colors[key],markeredgewidth =3,color = site_colors[key])
        ax[i].set_ylim(-0.1,1)
        ax[i].set_yticks(np.linspace(0,1, 11))
        ax[i].set_yticklabels(np.round(np.linspace(0,1, 11),1))
        if q==1:
            ax[i].set_ylabel("$\\langle S_1(A,B)\\rangle_B$", fontsize = 35)
        if q==2:
            ax[i].set_ylabel("$\\langle S_2(A,B)\\rangle_B$", fontsize = 35)
        if q==0:
            ax[i].set_ylabel("$\\langle S_0(A,B)\\rangle_B$", fontsize = 35)
        fig.legend(loc='upper center',fancybox=False,bbox_to_anchor=(0.5,0), shadow=False,ncol=5,title = "A")
        plt.tight_layout()
        plt.savefig(f"./figures/{dbname}/{pcol}/Fig6.eps", bbox_inches = "tight")
        plt.savefig(f"./figures/{dbname}/{pcol}/Fig6.pdf", bbox_inches = "tight")
        plt.savefig(f"./figures/{dbname}/{pcol}/Fig6.svg", bbox_inches = "tight")
        plt.savefig(f"./figures/{dbname}/{pcol}/Fig6.png", bbox_inches = "tight")
        



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
    
    
    
    ###################
    # Table replacement
    ###################
    # graph_list =[[0, 'LM II', 'LM III A1', 0.36850323937820184],
    #  [0.5, 'LM II', 'LM III A1', 0.5169973358901473],
    #  [1, 'LM II', 'LM III A1', 0.6350543067014085],
    #  [2, 'LM II', 'LM III A1', 0.724621225495097],
    #  [0, 'LM III A1', 'LM III A2', 0.45574130461363005],
    #  [0.5, 'LM III A1', 'LM III A2', 0.5829699755694543],
    #  [1, 'LM III A1', 'LM III A2', 0.6728201724055703],
    #  [2, 'LM III A1', 'LM III A2', 0.7267556766980137],
    #  [0, 'LM III A2', 'LM III B1', 0.2159211219447572],
    #  [0.5, 'LM III A2', 'LM III B1', 0.3182786126849091],
    #  [1, 'LM III A2', 'LM III B1', 0.41304593443751564],
    #  [2, 'LM III A2', 'LM III B1', 0.45089638901740403],
    #  [0, 'LM III B1', 'LM III B2', 0.059867024587612824],
    #  [0.5, 'LM III B1', 'LM III B2', 0.09993757112406364],
    #  [1, 'LM III B1', 'LM III B2', 0.13627016466505842],
    #  [2, 'LM III B1', 'LM III B2', 0.14712327905128134]]


    # vnames = list(set(db[pcol]))#['LM II' , 'LM III A1' , 'LM III A2', 'LM III B1', 'LM III B2']
    # q_color = {0: "tab:blue", 0.5: "tab:orange", 1: "tab:purple", 2:"tab:red" }
    # options = {"edgecolors": "tab:gray", "node_size": 800, "alpha": 1}
    
    # if dbname == "STANDARD_DATES_SettlementTomb_new2022" :
    #     pos = {'LM II':  np.array([-1,-1]) , 
    #      'LM IIIA': np.array([-1/3,-1/3]) , 
    #      'LM IIIB': np.array([1/3, 1/3]),
    #      'LM IIIC': np.array([1,1])}
        
    # else: # dbname == "NoEarlyDates_WorkingDB_Modelled":
    #     pos = {'LM II':  np.array([-1,-1]) , 
    #      'LM III A1': np.array([-0.5,-0.5]) , 
    #      'LM III A2': np.array([0, 0]),
    #      'LM III B1': np.array([0.5, 0.5]),
    #      'LM III B2': np.array([1,1])}

    # fig,ax = plt.subplots(1,4,figsize =(19,5))
    # i = 0
    # for q in [0,0.5,1,2]:
    #     g = nx.Graph()
    #     widths = []
    #     for item in graph_list: 
    #         if item[0] == q:    
    #             g.add_edge(item[1] , item[2], weight = item[-1])
    #             widths.append( item[-1] * 10/0.724621225495097)
                
    #     nx.draw_networkx_nodes(g, pos, nodelist=vnames, node_color=q_color[q], ax = ax[i], **options)
    #     nx.draw_networkx_edges(g,pos, width=widths , alpha=0.5, edge_color=q_color[q],ax = ax[i] )
    #     nx.draw_networkx_labels(g, pos=pos,ax = ax[i],
    #                             labels=dict(zip(vnames,vnames)),
    #                             font_color='black',font_size=20)
    #     # ax[i].box(False)

    #     at = AnchoredText(
    #         f"q={q}", prop=dict(size=20), frameon=False, loc='upper left')
    #     # at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    #     ax[i].add_artist(at)
    #     ax[i].spines['top'].set_visible(False)
    #     ax[i].spines['right'].set_visible(False)
    #     ax[i].spines['bottom'].set_visible(False)
    #     ax[i].spines['left'].set_visible(False)
    #     ax[i].set_ylim(-1.4,1.4)
    #     ax[i].set_xlim(-1.4,1.4)
    #     i +=1
    # plt.tight_layout()
    # plt.savefig(f"./figures/{dbname}/{pcol}/inter_period_similarity.svg")
    # plt.savefig(f"./figures/{dbname}/{pcol}/inter_period_similarity.pdf")
    # plt.savefig(f"./figures/{dbname}/{pcol}/inter_period_similarity.eps")
    # plt.savefig(f"./figures/{dbname}/{pcol}/inter_period_similarity.png")
    # plt.show()
            
            
