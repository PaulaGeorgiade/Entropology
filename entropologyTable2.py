"""
Table 2 Entropology JAMT

Created on Tue Jun  6 13:58:53 2023

@author: Tim Evans
"""


"""
Table 2 Entropology

Period 1	Period 2	q=0	q=0.5	q=1	q=2
LM II	LM III A1	0.37\pm0.17	0.52\pm0.15	0.64\pm0.13	0.72 \pm\ 0.14
LM III A1	LM III A2	0.46\pm0.12	0.58 \pm\ 0.11	0.67 \pm\ 0.12	0.73\ \pm\ 0.16
LM III A2	LM III B1	0.22\pm0.23	0.32\ \pm\ 0.26	0.41 \pm\ 0.3	0.45\ \pm\ 0.35
LM III B1	LM III B2	0.06\pm0.16	0.10 \pm\ 0.19	0.14\ \pm\ 0.23	0.15\ \pm\ 0.26

"""

import os    
import matplotlib.pyplot as plt
from mycolorpy import colorlist as mcp
#import matplotlib.transforms as transforms
plt.rcParams.update({'font.size': 30, "font.family":"helvetica"})

### USER data and alterable parameters

# Rotate horizontal axis labels and alter font size appropriately

# directory for output
output_directory= os.getcwd() + "//figures/Entropology_Dataset_Flattened/Solo_Period" #r'D:\DATA\Artefact\output'

# USe to form names of ouput files
rootname="Fig7"


    
rotateOn=False

qvalue_list = [  r"$q=0$", r"$q=0.5$", r"$q=1$", r"$q=2$" ]

period_string = "Period 1 - 2"
period_list = [ "LM II -\n LM IIIA1",  
                "LM IIIA1 -\n LM IIIA2",
                "LM IIIA2 -\n LM IIIB1",
                "LM IIIB1 -\n LM IIIB2" ]

results_list = [ [(0.37, 0.17), (0.52, 0.15), (0.64, 0.13), (0.72, 0.14)], 
                 [(0.46, 0.12), (0.58, 0.11), (0.67, 0.12), (0.73, 0.16)], 
                 [(0.22, 0.23), (0.32, 0.26), (0.41, 0.3 ), (0.45, 0.35)], 
                 [(0.06, 0.16), (0.10, 0.19), (0.14, 0.23), (0.15, 0.26)]
                ]

### END OPF USER DATA ###

def saveFigure(plt,filenameroot,extlist=['pdf'],messageString='Plot',screenOn=False):
    '''Save figure as file
    
    Input
    plt -- plot to be save
    filenameroot -- full name of file excpet for extension
    extlist=['pdf'] -- list of extensions to be used
    messageString='Plot' -- message to print out, none if empty string
    '''
    for ext in extlist:
        if filenameroot.endswith('.'):
            plotfilename=filenameroot+ext
        else:
            plotfilename=filenameroot+'.'+ext
        if len(messageString)>0:
            print (messageString+' file '+plotfilename)
        plt.savefig(plotfilename)
    if screenOn:
        plt.show()


linestyle_list = [ 'solid', 'solid', 'solid', 'solid']
marker_list = [ 'o', 'o', 'o', 'o']

# See https://matplotlib.org/stable/gallery/color/named_colors.html
# and https://matplotlib.org/stable/gallery/color/color_demo.html
# colour_list = [ 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']
colour_list = mcp.gen_color(cmap="viridis",n=4)



results_mean =[]
results_error =[]

for pindex in range(len(period_list)):
    results_mean.append([None]*len(qvalue_list))
    #results_mean[pindex].append([])
    results_error.append([None]*len(qvalue_list))
    #results_error[pindex].append([])
    for qindex in range(len(qvalue_list)):
        mean = results_list[pindex][qindex][0]
        results_mean[pindex][qindex] = mean
        error=results_list[pindex][qindex][1]
        results_error[pindex][qindex] = error

# https://matplotlib.org/stable/gallery/lines_bars_and_markers/categorical_variables.html
#fig, axs = plt.subplots(1, 1, figsize=(9, 3), sharey=True)

fig, ax = plt.subplots(1, 1, figsize=(8, 6))
number_categories = len(period_list)
ax.yaxis.grid(True,which='major')
offset_base_value = 20
offset_increment = offset_base_value/number_categories
offset_value= -offset_base_value*(number_categories-1)/2
for pindex in range(number_categories):
    #ax.scatter(period_list, results_mean[pindex][:], label=qvalue_list[pindex])
    xvalues = [x+(pindex-(number_categories-1)/2)/10 for x in range(number_categories)]
    ax.errorbar(xvalues, results_mean[pindex][:], 
                linestyle = linestyle_list[pindex],
                color=colour_list[pindex],
                yerr = results_error[pindex][:], 
                label=qvalue_list[pindex], capsize = 5, marker = marker_list[pindex], markersize = 12 )
                #transform=trans+offset(-5))

# See https://stackoverflow.com/questions/43152502/how-can-i-rotate-xticklabels-in-so-the-spacing-between-each-xticklabel-is-equal
plt.xticks(range(number_categories))

if rotateOn:
    ax.set_xticklabels( period_list, rotation = 90,fontsize=18)
    rootname=rootname+"90"
else:
    ax.set_xticklabels( period_list, fontsize=18)


ax.tick_params(axis='y', labelsize=18)
    
ax.legend(loc='upper left',fontsize=18)
#fig.suptitle('Categorical Plotting')

#input_directory=r'..\input'
filenameroot=os.path.join( output_directory, rootname)
saveFigure(plt,filenameroot,extlist=['pdf','svg','jpg', 'eps'])
