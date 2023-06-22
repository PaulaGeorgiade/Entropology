# Author Henry Price, Imperial College London
#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import os


output_directory = r"D:\DATA\artefact\output"


plt.rcParams["figure.figsize"] = (6,6)

data = [4.053236001,np.nan,np.nan,7.319310267,6.814215858,8.238599677,5.924414781,5.320974069,5.488835819,4.053251907]
xs = np.arange(1, len(data) +1 )
s1 = np.array(data).astype(np.double)
print(s1)
print(xs)
s1mask = np.isfinite(s1)
print(s1mask)

ax = plt.subplot(111)
plt.plot(xs[s1mask], s1[s1mask], linestyle='-', marker='o')


plt.xticks(xs)
plt.ylabel("Diversity",fontsize= 12) #rename if using different q
plt.xlabel("Time Units",fontsize= 12) #rename if using different q

# # Move left and bottom spines outward by 10 points
# ax.spines['left'].set_position(('outward', 10))
# ax.spines['bottom'].set_position(('outward', 10))
# # Hide the right and top spines
# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)

# Only show ticks on the left and bottom spines
# ax.yaxis.set_ticks_position('left')
# ax.xaxis.set_ticks_position('bottom')

plt.tight_layout()
filenameroot = os.path.join(output_directory,"Fig3a_temp")
print("*** Saving files to "+filenameroot+".*")
plt.savefig(filenameroot+".pdf")
plt.savefig(filenameroot+".svg")
plt.savefig(filenameroot+".tiff")
plt.savefig(filenameroot+".eps")
plt.show()


# ![Picture title](image-20220825-161213.png)

# In[2]:


# effective_aggregation= {'LM II': 8.278410883904517, 'LM III A1': 12.790514690646805, 'LM III A2': 10.584934829964554, 'LM III B1': 6.30873351413355, 'LM III B2': 4.202394007290234}
# landscape_aggregation = {'LM II': 10.510587378081292, 'LM III A1': 13.679987996543773, 'LM III A2': 10.279571400225047, 'LM III B1': 10.93223256170765, 'LM III B2': 7.342897951985194}

effective_aggregation = {'LM II': 8.27841088390452, 'LM III A1': 9.857139161788577, 'LM III A2': 10.584934829964551, 'LM III B1': 6.308733514133549, 'LM III B2': 4.202394007290237}
landscape_aggregation =  {'LM II': 10.510587378081286, 'LM III A1': 10.638897763177958, 'LM III A2': 10.279571400225047, 'LM III B1': 10.932232561707654, 'LM III B2': 7.342897951985197}


plt.rcParams["figure.figsize"] = (6,6)

data =  pd.DataFrame(effective_aggregation.items())
data["Landscape Aggregation"] = landscape_aggregation.values()
print(data)
data.columns = ["Period", "Effective Aggregation", "Landscape Aggregation"]
print(data)
# data = data.set_index("Period")
# print(data)
ax = plt.subplot(111)

# ax.plot(D.keys(),D.values(),marker ="^",markersize= 10, linestyle = "--",color= "crimson")
# plt.plot(s1, linestyle='--', marker='o',color= "crimson")
plt.plot(data["Period"], data["Effective Aggregation"], linestyle='-.', marker='^',color= "crimson", label = "Effective Aggregation")
plt.plot(data["Period"], data["Landscape Aggregation"], linestyle='-', marker='o', label = "Landscape Aggregation")


plt.ylabel("Diversity",fontsize= 12 ) #rename if using different q
plt.xlabel("Time Periods",fontsize= 12) #rename if using different q




# # Move left and bottom spines outward by 10 points
# ax.spines['left'].set_position(('outward', 10))
# ax.spines['bottom'].set_position(('outward', 10))
# # Hide the right and top spines
# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)

# Only show ticks on the left and bottom spines
# ax.yaxis.set_ticks_position('left')
# ax.xaxis.set_ticks_position('bottom')

plt.legend()
plt.tight_layout()
filenameroot = os.path.join(output_directory,"Fig3b")
print("*** Saving files to "+filenameroot+".*")
plt.savefig(filenameroot+".pdf")
plt.savefig(filenameroot+".svg")
plt.savefig(filenameroot+".tiff")
plt.savefig(filenameroot+".eps")
plt.show()


# In[3]:


fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12, 4)  ) #sharey=True)
font = {'family':'helvetica','color':'black',"size": 13}
font1 = {'family':'helvetica','color':'black'}
plt.rcParams['axes.titley'] = 1.0 
plt.rcParams['axes.titlepad'] = -16 
ax1.plot(data["Period"], data["Effective Aggregation"], linestyle='-.', marker='^',color= "crimson", label = "Effective Aggregation")
ax1.plot(data["Period"], data["Landscape Aggregation"], linestyle='-', marker='o', color="#1f77b4", label = "Landscape Aggregation")
ax0.plot(xs[s1mask][1:], s1[s1mask][1:], linestyle='-', marker='o',color= '#1f77b4')
ax0.plot(xs[s1mask][0:2], s1[s1mask][0:2], linestyle='-.',  marker='o',color= '#1f77b4')

ax0.set_title("   (a)", fontdict = font1, loc='left')
ax1.set_title("   (b)", fontdict = font1, loc='left')
# Set common labels
ax0.set_xlabel("Time Units", fontdict = font)
ax1.set_xlabel("Time Periods", fontdict = font)
ax0.set_ylabel("Diversity", fontdict = font)
ax1.set_ylabel(r"$D_{1}^{\gamma}$", fontdict = font)
ax0.set_xticks(xs)
# ax1.spines['right'].set_visible(False)
# ax1.spines['top'].set_visible(False)
# ax0.spines['right'].set_visible(False)
# ax0.spines['top'].set_visible(False)

plt.legend()
plt.tight_layout()

filenameroot = os.path.join(output_directory,"Fig3")
print("*** Saving files to "+filenameroot+".*")
plt.savefig(filenameroot+".pdf")
plt.savefig(filenameroot+".svg")
plt.savefig(filenameroot+".tiff")
plt.savefig(filenameroot+".eps")
plt.show()



# <a style='text-decoration:none;line-height:16px;display:flex;color:#5B5B62;padding:10px;justify-content:end;' href='https://deepnote.com?utm_source=created-in-deepnote-cell&projectId=b220710f-d6b0-4f90-9f8c-6c46d7a2a478' target="_blank">
# <img alt='Created in deepnote.com' style='display:inline;max-height:16px;margin:0px;margin-right:7.5px;' src='data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iODBweCIgaGVpZ2h0PSI4MHB4IiB2aWV3Qm94PSIwIDAgODAgODAiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+CiAgICA8IS0tIEdlbmVyYXRvcjogU2tldGNoIDU0LjEgKDc2NDkwKSAtIGh0dHBzOi8vc2tldGNoYXBwLmNvbSAtLT4KICAgIDx0aXRsZT5Hcm91cCAzPC90aXRsZT4KICAgIDxkZXNjPkNyZWF0ZWQgd2l0aCBTa2V0Y2guPC9kZXNjPgogICAgPGcgaWQ9IkxhbmRpbmciIHN0cm9rZT0ibm9uZSIgc3Ryb2tlLXdpZHRoPSIxIiBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPgogICAgICAgIDxnIGlkPSJBcnRib2FyZCIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyMzUuMDAwMDAwLCAtNzkuMDAwMDAwKSI+CiAgICAgICAgICAgIDxnIGlkPSJHcm91cC0zIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgxMjM1LjAwMDAwMCwgNzkuMDAwMDAwKSI+CiAgICAgICAgICAgICAgICA8cG9seWdvbiBpZD0iUGF0aC0yMCIgZmlsbD0iIzAyNjVCNCIgcG9pbnRzPSIyLjM3NjIzNzYyIDgwIDM4LjA0NzY2NjcgODAgNTcuODIxNzgyMiA3My44MDU3NTkyIDU3LjgyMTc4MjIgMzIuNzU5MjczOSAzOS4xNDAyMjc4IDMxLjY4MzE2ODMiPjwvcG9seWdvbj4KICAgICAgICAgICAgICAgIDxwYXRoIGQ9Ik0zNS4wMDc3MTgsODAgQzQyLjkwNjIwMDcsNzYuNDU0OTM1OCA0Ny41NjQ5MTY3LDcxLjU0MjI2NzEgNDguOTgzODY2LDY1LjI2MTk5MzkgQzUxLjExMjI4OTksNTUuODQxNTg0MiA0MS42NzcxNzk1LDQ5LjIxMjIyODQgMjUuNjIzOTg0Niw0OS4yMTIyMjg0IEMyNS40ODQ5Mjg5LDQ5LjEyNjg0NDggMjkuODI2MTI5Niw0My4yODM4MjQ4IDM4LjY0NzU4NjksMzEuNjgzMTY4MyBMNzIuODcxMjg3MSwzMi41NTQ0MjUgTDY1LjI4MDk3Myw2Ny42NzYzNDIxIEw1MS4xMTIyODk5LDc3LjM3NjE0NCBMMzUuMDA3NzE4LDgwIFoiIGlkPSJQYXRoLTIyIiBmaWxsPSIjMDAyODY4Ij48L3BhdGg+CiAgICAgICAgICAgICAgICA8cGF0aCBkPSJNMCwzNy43MzA0NDA1IEwyNy4xMTQ1MzcsMC4yNTcxMTE0MzYgQzYyLjM3MTUxMjMsLTEuOTkwNzE3MDEgODAsMTAuNTAwMzkyNyA4MCwzNy43MzA0NDA1IEM4MCw2NC45NjA0ODgyIDY0Ljc3NjUwMzgsNzkuMDUwMzQxNCAzNC4zMjk1MTEzLDgwIEM0Ny4wNTUzNDg5LDc3LjU2NzA4MDggNTMuNDE4MjY3Nyw3MC4zMTM2MTAzIDUzLjQxODI2NzcsNTguMjM5NTg4NSBDNTMuNDE4MjY3Nyw0MC4xMjg1NTU3IDM2LjMwMzk1NDQsMzcuNzMwNDQwNSAyNS4yMjc0MTcsMzcuNzMwNDQwNSBDMTcuODQzMDU4NiwzNy43MzA0NDA1IDkuNDMzOTE5NjYsMzcuNzMwNDQwNSAwLDM3LjczMDQ0MDUgWiIgaWQ9IlBhdGgtMTkiIGZpbGw9IiMzNzkzRUYiPjwvcGF0aD4KICAgICAgICAgICAgPC9nPgogICAgICAgIDwvZz4KICAgIDwvZz4KPC9zdmc+' > </img>
# Created in <span style='font-weight:600;margin-left:4px;'>Deepnote</span></a>
