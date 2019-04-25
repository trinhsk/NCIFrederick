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
    axis.set_title(f'{dfm.columns[cnt]}',fontsize=7.6)
    axis.title.set_position([.5, .85])
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
    dfm_array = np.array(dfm).reshape(16,colCnt)
    nphist = np.linspace(min_df,max_df,num=18)
    colourBlue = [ '#E3E6E8', '#E0E7EB', '#DEE8ED', '#DBE9F0', '#D9EAF2', '#D6EBF5', '#D4EBF7', '#D1ECFA', '#CFEDFC', '#CCEEFF', '#A8D8F0', '#A3DAF5', '#9EDBFA', '#99DDFF', '#7DC4E8', '#75C7F0', '#6EC9F7', '#66CCFF' ]
    lamDiff = lambda x: [abs(x-i) for i in nphist].index(min([abs(x-i) for i in nphist]))
    colours=[]
    for i in range(dfm_array.shape[0]):
        for j in range(dfm_array.shape[1]):
            if dfm_array[i,j] < 0:
                colours.append('#5C6970')
            else:
                colours.append(colourBlue[lamDiff(dfm_array[i,j])])
    xs = list(map(lambda x: [x]*16,list(range(24)))) 
    xs = [str(item) for sublist in xs for item in sublist] #flatten list
    strings = [i for i in string.ascii_uppercase[0:16]]*colCnt
    df = pd.DataFrame({'xs':xs,'ys':strings,'value':dfm_array.flatten('C').tolist(),'colour':colours})
    p = figure(plot_width=900,plot_height=600,x_axis_location="above", tools="hover",
               title=f'Heatmap of {pltcode} 384-plate at {int(wavelength)}nm', 
               x_range=df['xs'].drop_duplicates(),#[str(i) for i in range(24)],
               y_range=list(reversed(df['ys'].drop_duplicates())),#list(reversed([i for i in string.ascii_uppercase[:16]])),
               tooltips = [('wellID', '@ys,@xs'), ('abs', '@value')])
    p.rect('xs', 'ys', 0.9, 0.9,source=ColumnDataSource(df), fill_color='colour',line_color='black')
    p.xaxis.major_label_text_font_style='bold'
    p.yaxis.major_label_text_font_style='bold'
    label_dict = {}
    for i, s in enumerate(df['xs'].drop_duplicates()):
        label_dict[i] = str(int(s) + 1)
    p.xaxis.formatter = FuncTickFormatter(code=""" 
        var labels = %s;
        return labels[tick];
    """ % label_dict) #change x-axis tick labels
    return p
