import matplotlib
import pandas as pd
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.offsetbox import AnchoredText
from diversity_calculators import calc_diversity , calc_gamma_diversity , calc_alpha_diversity , calc_beta_diversity
plt.rcParams.update({'font.size': 30, "font.family":"helvetica"})
    
def read_df (exclude_periods = ["LM", "LM III", "LM III A", "LM III B"], dbname = "STANDARD_DATES_SettlementTomb_new2022",pcol = "New Merged Dates", map_periods = False):
    """
    This function loads the data file and plots a histogram of abundance of species
    """
    period_map = {'LM': 'LM', "LM II" : "LM II", 'LM III': "LM III", 'LM III A': "LM III A", 'LM III A1':'LM III A1' ,
                  'LM III A1 Early': "LM III A1", 'LM III A2':'LM III A2' ,'LM III A2 Early':'LM III A2',
                  'LM III A2 Late': 'LM III A2', 'LM III B': 'LM III B','LM III B1':'LM III B1', 'LM III B2':'LM III B2'}
    print("using ", dbname, pcol )
    db = pd.read_excel(f"{dbname}.xlsx")[["Deposition_Site","Vessel_Form", pcol]]
    for p in exclude_periods: 
        db = db[db[pcol] != p]
    print("set of periods", set(db[pcol]))
    if map_periods :
        print("mapping periods")
        db[pcol]= db[pcol].map(period_map)
    db = db[db.Vessel_Form!= "Unknown"]
    db =db.dropna()
    print("length of database:" ,len(db) )
    return db

    
    
    ###############
    # Histogram of period sizes
    ###############
    # fig,ax = plt.subplots(1,1,figsize=(10,10))
    # y = []
    # x = []
    # for p,df in db.groupby("Solo_Period"):
    #     y.append( len(df))
    #     x.append(p)
    # df = pd.DataFrame([x,y]).T
    # df.columns = ["Date",1]
    # df.index= df["Date"]
    # df[1].plot.bar(rot=0,ax = ax)
    # plt.xticks(rotation=90)
    # ax.title.set_text("Total number of artefacts")
    # plt.tight_layout()
    # plt.savefig(f"./figures/{dbname}/{pcol}/period_size.pdf")
    # plt.show()
    

def run_beta(db, dbname, pcol):
    """
    Plotting function to visualise Beta diversity
    """
    for q in [0.5,1,2]:
        D_beta_land = {}
        D_beta_eff= {}
        for p in sorted(set(db[pcol])):
            samples = [list(group["Vessel_Form"]) for site,group in db[db[pcol] ==p].groupby("Deposition_Site")]
            D_beta_land[p]=calc_beta_diversity(samples, q,False)
            D_beta_eff[p]=calc_beta_diversity(samples, q,True)
        fig,ax = plt.subplots(1,1,figsize=(12,10))
        ax.plot(D_beta_land.keys(),D_beta_land.values(),marker ="o",markersize= 20,color="black", label = "Landscape")
        ax.plot(D_beta_eff.keys(),D_beta_eff.values(),marker ="s",markersize= 20,color="red", label = "Effective")
        ax.tick_params(axis="x",rotation = 90)
        ax.title.set_text("$^{}D_\\beta$".format(str(q)))  
        ax.set_ylim(0,5)
        plt.legend(loc=1)
        plt.tight_layout()
        plt.savefig(f"./figures/{dbname}/{pcol}/beta_diversity_landscape_and_effective_q_{q}.pdf")
        plt.savefig(f"./figures/{dbname}/{pcol}/beta_diversity_landscape_and_effective_q_{q}.svg")
        plt.savefig(f"./figures/{dbname}/{pcol}/beta_diversity_landscape_and_effective_q_{q}.eps")
    
def run_alpha(db, dbname, pcol):
    """
    Plotting function to visualise Alpha diversity
    """
    for q in [0.5,1,2]:
        D_alpha_land = {}
        D_alpha_eff= {}
        for p in sorted(set(db[pcol])):
            print(p)
            samples = [list(group["Vessel_Form"]) for site,group in db[db[pcol] ==p].groupby("Deposition_Site")]
            D_alpha_land[p]=calc_alpha_diversity(samples, q,False)
            D_alpha_eff[p]=calc_alpha_diversity(samples, q,True)
        fig,ax = plt.subplots(1,1,figsize=(12,10))    
        ax.plot(D_alpha_land.keys(),D_alpha_land.values(),marker ="o",markersize= 20,color="black", label = "Landscape")
        ax.plot(D_alpha_eff.keys(),D_alpha_eff.values(),marker ="s",markersize= 20,color="red", label = "Effective")
        ax.tick_params(axis="x",rotation = 90)
        ax.title.set_text("$^{}D_\\alpha$".format(str(q)))  
        ax.set_ylim(0,15)
        plt.legend(loc=3)
        plt.tight_layout()
        plt.savefig(f"./figures/{dbname}/{pcol}/alpha_diversity_landscape_and_effective_q_{q}.pdf")
        plt.savefig(f"./figures/{dbname}/{pcol}/alpha_diversity_landscape_and_effective_q_{q}.svg")
        plt.savefig(f"./figures/{dbname}/{pcol}/alpha_diversity_landscape_and_effective_q_{q}.eps")
    
def run_gamma(db , q = 1,dbname = "NoEarlyDates_WorkingDB_Modelled" ,pcol = "Solo_Period", figname= "Fig3"):
    """
    Plotting function to visualise Gamma diversity
    """
    fig,ax = plt.subplots(1,1,figsize=(14,9))
    D={}
    for p in sorted(set(db[pcol])):
        samples = [list(group["Vessel_Form"]) for site,group in db[db[pcol] ==p].groupby("Deposition_Site")]
        D[p]=calc_gamma_diversity(samples, q,True)     
    ax.plot(D.keys(),D.values(),marker ="o",markersize= 20, label = "Effective", linestyle= "-", linewidth=3,color= "royalblue")
    D={}
    for p in sorted(set(db[pcol])):
        samples = [list(group["Vessel_Form"]) for site,group in db[db[pcol] ==p].groupby("Deposition_Site")]
        D[p]=calc_gamma_diversity(samples, q,False)
    ax.plot(D.keys(),D.values(),marker ="^",markersize= 20, label = "Landscape", linestyle = "--", linewidth=3,color= "crimson")
    ax.set_xticks(list(range(len(set(db[pcol])))), list(D.keys()), rotation=0)
    ax.tick_params(axis = "both", length = 10, width=2  , which = "both")
    ax = plt.gca()
    ax.grid(which='major', axis='y', linestyle='-' ,lw =2)
    ax.set_ylim(1,15)
    ax.set_ylabel("$D^{\\gamma}_{1}$",fontsize= 40)
    ax.set_xlabel("Time Periods")
    plt.legend(loc=1)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(f"./figures/{dbname}/{pcol}/{figname}.pdf")
    plt.savefig(f"./figures/{dbname}/{pcol}/{figname}.svg")
    plt.savefig(f"./figures/{dbname}/{pcol}/{figname}.eps")
        
def random_replacement(db, sample, percentage, uniform = False):
    """
    Takes in a list of samples and replaces a percentage of the sample by a random 
    set of artefacts taken from the database db either uniformly (each sample has equal probability
    to be chosen), or in proportion to the species abundance.
    """
    num_to_replace = int(np.ceil(len(sample)*percentage))
    all_artefacts= list(db.Vessel_Form)
    if uniform:
        set_artefacts = set(db.Vessel_Form)
        all_artefacts = []
        for a in set_artefacts:
            all_artefacts += [a for i in range(1000)]
    sample_copy = sample.copy()
    random.shuffle(sample_copy)
    sample_copy = sample_copy[:-num_to_replace]
    sample_copy += random.sample(all_artefacts,num_to_replace)
    return sample_copy
    
def run_gamma_error(db,percentage=0.1,dbname=None, pcol=None,figname = None, ylimit = 45):
    """
    Plotting function to visualise Gamma diversity with errorbars
    """
    fig,axs = plt.subplots(1,2,figsize =(22,9))
    i = 0
    for ax in axs:
        if i==0:
            at = AnchoredText(
                "(a)", prop=dict(size=35), frameon=False, loc='upper left')
            ax.add_artist(at)
        else:
            at = AnchoredText(
                "(b)", prop=dict(size=35), frameon=False, loc='upper left')
            ax.add_artist(at)
        cols = {2:"#a62802",1: "#46a303",0.5:"#0266a1",0: "#b88702"}
        colran = {2:"#f73a00",1: "#5ede02", 0.5: "#03a1fc", 0:"#f5b402"}
        shapes = { 2: "s", 1: "^", 0.5: "o", 0: "D" }
        # linestyles = {2:"solid" , 1:"dotted" , 0.5: "dashed" , 0: "dashdot"}
        for q in [0,0.5,1,2]:
            D=defaultdict(list)
            for p in sorted(set(db[pcol])):
                samples = [list(g["Vessel_Form"]) for v,g in db[db[pcol]==p].groupby("Deposition_Site")]
                for r in range(100):
                    samples_shuffled = []
                    for sample in samples:
                        samples_shuffled.append(random_replacement(db, sample,percentage))
                    D[p].append(calc_gamma_diversity(samples_shuffled, q,bool(i)))
                D[p].append(calc_gamma_diversity(samples,q,bool(i)))
            if i==0:
                ax.plot(D.keys(),[x[-1] for x in D.values()],marker = shapes[q], markersize= 30, markerfacecolor = "white",
                        label = "q={}".format(q),markeredgecolor=cols[q], color = cols[q])
                ax.errorbar(D.keys(),[np.mean(x[:-1]) for x in list(D.values())],[np.std(x[:-1]) for x in list(D.values())],
                            marker = shapes[q] , markersize= 20,capsize=8,label = "q={} randomised".format(q),color=colran[q],linestyle ="--")
            else:
                ax.plot(D.keys(),[x[-1] for x in D.values()],marker = shapes[q], markersize= 30, markerfacecolor = "white", 
                        markeredgecolor=cols[q], color = cols[q])
                ax.errorbar(D.keys(),[np.mean(x[:-1]) for x in list(D.values())],[np.std(x[:-1]) for x in list(D.values())],
                            marker = shapes[q] ,markersize= 20,capsize=8,linestyle ="--", color=colran[q])
        i+=1
        ax.set_ylabel("$D^{\\gamma}_q$",fontsize=40)
        ax.set_ylim(0,ylimit)
    fig.legend(loc='upper center',fancybox=False,bbox_to_anchor=(0.5, 0), shadow=False,ncol=4)
    plt.tight_layout()
    plt.savefig(f"./figures/{dbname}/{pcol}/{figname}.pdf", bbox_inches = "tight")
    plt.savefig(f"./figures/{dbname}/{pcol}/{figname}.svg", bbox_inches = "tight")
    plt.savefig(f"./figures/{dbname}/{pcol}/{figname}.eps", bbox_inches = "tight")

def run_site_error(db,q,dbname, pcol,percentage=0.1,plot_zeros=False):
    """
    Plotting function to visualise site diversity with errorbars
    """
    colors = {"Chania":"blue","Knossos":"orange","Mochlos":"red","Kommos":"green","Palaikastro":"purple"}
    markers = {"Chania":"o","Knossos":"v","Mochlos":"s","Kommos":"*","Palaikastro":"^"}
    if plot_zeros==False:
        min_val=0
    else:
        min_val= -1
    for site,df in db.groupby("Deposition_Site"):
        y = []
        x = []
        yerr = []
        y_true=[]
        for date in ["LM II", "LM III A1","LM III A2","LM III B1","LM III B2"]:
            X = df[df[pcol]==date]
            ytemp=[]
            sample =list(X.Vessel_Form)
            if len(sample)>min_val:
                for run in range(100):
                    try:
                        ytemp.append(calc_diversity(random_replacement(sample,percentage),q))
                    except:
                        ytemp.append(0)
                y.append(np.mean(ytemp))
                yerr.append(np.std(ytemp))
                try:
                    y_true.append(calc_diversity(X.Vessel_Form,q))
                except:
                    y_true.append(0)
            else:
                y.append(np.nan)
                yerr.append(np.nan)
                y_true.append(np.nan)
            x.append(date)
        fig,ax = plt.subplots(1,1,figsize=(10,8))
        ax.errorbar(x, y, yerr,label = site,linestyle = "--",marker = markers[site],markersize =20,linewidth = 1 ,color=colors[site],capsize=5)
        ax.plot(x, y_true,label = site,linestyle = "-",marker = markers[site],alpha=0.5,linewidth = 5 ,color=colors[site])
        ax.title.set_text(site)
        plt.xticks(x,rotation= 90)
        plt.ylim(0,20)
        plt.tight_layout()
        if plot_zeros==True:
            plt.savefig(f"./figures/{dbname}/{pcol}/site_diversity_q_{q}_{site}_shuffled_percentage_{percentage}.pdf")
            plt.savefig(f"./figures/{dbname}/{pcol}/site_diversity_q_{q}_{site}_shuffled_percentage_{percentage}.eps")
            plt.savefig(f"./figures/{dbname}/{pcol}/site_diversity_q_{q}_{site}_shuffled_percentage_{percentage}.svg")
        else:
            plt.savefig(f"./figures/{dbname}/{pcol}/site_diversity_q_{q}_{site}_shuffled_percentage_{percentage}_nozeros.pdf")
            plt.savefig(f"./figures/{dbname}/{pcol}/site_diversity_q_{q}_{site}_shuffled_percentage_{percentage}_nozeros.svg")
            plt.savefig(f"./figures/{dbname}/{pcol}/site_diversity_q_{q}_{site}_shuffled_percentage_{percentage}_nozeros.eps")
        plt.show()
        