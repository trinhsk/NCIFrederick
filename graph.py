import matplotlib.pyplot as plt
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.figure import Figure
import string
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, FuncTickFormatter
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
    fig = Figure(figsize=(0.6,0.6))
    axis = fig.add_subplot(1,1,1)
    absvals = dfm[f'{wellIds[cnt]}']
    axis.plot(wavelength,absvals)
    axis.set_title(f'{dfm.columns[cnt]}',fontsize=9)
    axis.title.set_position([.5, .6])
    axis.tick_params(
            which='both',
            bottom=False,
            left=False,
            labelbottom=False,
            labelleft=False)
    FigureCanvasSVG(fig).print_svg(img)
    return img.getvalue()

def build_heatmap(dfm,row,wavelength,pltcode):
    dfm = dfm.iloc[row,:]
    max_df = dfm.max().max()
    min_df = abs(dfm).min().min()
    colCnt = int(len(dfm)/16)
    dfm_array = np.array(dfm).reshape(16,colCnt).T
    colourBlue = [ '#E3E6E8', '#E0E7EB', '#DEE8ED', '#DBE9F0', '#D9EAF2', '#D6EBF5', '#D4EBF7', '#D1ECFA', '#CFEDFC', '#CCEEFF', '#A8D8F0', '#A3DAF5', '#9EDBFA', '#99DDFF', '#7DC4E8', '#75C7F0', '#6EC9F7', '#66CCFF' ]
    nphist = np.linspace(min_df,max_df,num=len(colourBlue))
    lamDiff = lambda x: [abs(x-i) for i in nphist].index(min([abs(x-i) for i in nphist]))
    colours=[]
    for i in range(dfm_array.shape[0]):
        for j in range(dfm_array.shape[1]):
            if dfm_array[i,j] < 0:
                colours.append('#5C6970')
            else:
                colours.append(colourBlue[lamDiff(dfm_array[i,j])])
    xs = list(map(lambda x: [x]*16,list(range(24))))
    xs = [str(item+1) for sublist in xs for item in sublist] #flatten list
    strings = [i for i in string.ascii_uppercase[0:16]]*colCnt
    df = pd.DataFrame({'xs':xs,'ys':strings,'value':dfm_array.flatten('C'),'colour':colours})
    p = figure(plot_width=1600,plot_height=1170,x_axis_location="above", tools="hover",
               # title=f'Heatmap of {pltcode} 384-plate at {int(wavelength)}nm', 
               sizing_mode='scale_width',
               x_range=df['xs'].drop_duplicates(),#[str(i) for i in range(24)],
               y_range=list(reversed(df['ys'].drop_duplicates())),#list(reversed([i for i in string.ascii_uppercase[:16]])),
               tooltips = [('wellID', '@ys,@xs'), ('abs', '@value')])
    p.rect('xs', 'ys', .64,.64 ,source=ColumnDataSource(df), fill_color='colour',line_color='black')
    p.toolbar.logo = None
    p.toolbar_location = None
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    label_dict = {}
    for i, s in enumerate(df['xs'].drop_duplicates()):
        label_dict[i] = str(int(s) + 1)
    return p


def corrAbs(dfm1,dfm2,row):
    dfmcrude = dfm1.iloc[row,:]
    dfmfx = dfm2.iloc[row,:]
    darray_crude = np.array(dfmcrude).reshape(16,24)
    darray_fx = np.array(dfmfx).reshape(16,24)
    darray_t = np.flip(np.flip(darray_crude.T,axis=1),axis=0).reshape(16,24) #flip the 100 plate
    ar_crude = np.delete(np.delete(np.delete(darray_crude, np.s_[1::2], 1),[0],1),np.s_[1::2],0) #filter elements so that only obtain the first value of each quadrant
    ar_crude_t = np.delete(np.delete(np.delete(darray_t, np.s_[1::2], 1),[0],1),np.s_[1::2],0) #filter elements as above but for tranposed plate
    ar_fx7 = np.delete(np.delete(np.delete(darray_fx, np.s_[::2], 1),[0],1),np.s_[0::2],0) #filter elemnts for 7th fx
    ar_fx6 = np.delete(np.delete(np.delete(darray_fx, np.s_[1::2], 1),[0],1),np.s_[0::2],0)
    corr6 = (np.corrcoef(ar_crude.flatten(),ar_fx6.flatten())[0][1],np.corrcoef(ar_crude_t.flatten(),ar_fx6.flatten())[0][1])
    corr7 = (np.corrcoef(ar_crude.flatten(),ar_fx7.flatten())[0][1],np.corrcoef(ar_crude_t.flatten(),ar_fx7.flatten())[0][1])
    return (corr6,corr7)
