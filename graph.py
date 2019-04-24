import matplotlib.pyplot as plt
import io
import base64
import numpy as np
import pandas as pd
import string
 

wellIds=[]
for i in range(1,25):
    for j in range(1,25):
        wellIds.append(f'{chr(64+i)}{j}')



def build_graph(dfm):
    img = io.BytesIO()

    fig, ax = plt.subplots(16,24,figsize=(20,17))
    fig.subplots_adjust(wspace=0.5,hspace=0.85)
    cnt=0
    dfm_strip = dfm.drop(dfm.columns[0], axis=1) #remove wavelength
    dfm_strip = dfm_strip.drop(dfm.columns[1], axis=1) #remove temperature
    dfm_strip = dfm_strip.drop(dfm.columns[len(dfm.columns)-1],axis=1) #remove last NaN column
    for i in range(16):
        for j in range(24):
            ax[i,j].plot(dfm.Wavelength,
                         dfm_strip[f'{wellIds[cnt]}'],    
                        )
            ax[i,j].set_title(f'{dfm_strip.columns[cnt]}')
            ax[i,j].title.set_position([.5, .8])
            ax[i,j].tick_params(
                which='both',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                left=False,         # ticks along the top edge are off
                labelbottom=False,
                labelleft=False)
            cnt+=1

    fig.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    fig.close()
    return 'data:image/png;base64,{}'.format(graph_url)
