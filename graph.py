import matplotlib.pyplot as plt
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.figure import Figure
import io
import numpy as np
import pandas as pd
import string

wellIds=[]
for i in range(1,25):
    for j in range(1,25):
        wellIds.append(f'{chr(64+i)}{j}')

def stripDF(dfm):
    dfm_strip = dfm.drop(dfm.columns[0], axis=1) #remove wavelength
    dfm_strip = dfm_strip.drop(dfm.columns[1], axis=1) #remove temperature
    dfm_strip = dfm_strip.drop(dfm.columns[len(dfm.columns)-1],axis=1) #remove last NaN column
    return dfm_strip

def build_graph(dfm,wavelength,cnt):
    img = io.BytesIO()
    fig = Figure(figsize=(1,1))

    axis = fig.add_subplot(1,1,1)
    
    absvals = dfm[f'{wellIds[cnt]}'] 
    axis.plot(wavelength,absvals)
    axis.set_title(f'{dfm.columns[cnt]}',fontsize=10)
    axis.title.set_position([.5, .92])
    axis.tick_params(
            which='both',
            bottom=False,
            left=False,
            labelbottom=False,
            labelleft=False)
    FigureCanvasSVG(fig).print_svg(img)
    return img.getvalue()
