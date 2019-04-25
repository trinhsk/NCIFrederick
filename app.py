from flask import Flask, render_template, Response, Markup, send_file
from graph import build_graph, build_heatmap, pd, stripDF
from bokeh.embed import components

app = Flask(__name__)

dfm100 = pd.read_csv(app.root_path + "/textfiles/14190301100.txt",encoding='utf-16',sep='\t',skiprows=2,skipfooter=2,engine='python')
dfm100 = stripDF(dfm100)

dfm200 = pd.read_csv(app.root_path+ '/textfiles/14190301200.txt',encoding='utf-16',sep='\t',skiprows=2,skipfooter=2,engine='python')
dfm200 = stripDF(dfm200)

wavelength = list(range(220,810,10))

lstofplots100 = []
for i in range(384):
    lstofplots100.append(Markup(build_graph(dfm100,wavelength,i).decode('utf-8')))

@app.route('/')
def plotgraphs():
    p = build_heatmap(dfm100,1,250,'14109130211')
    script,div = components(p)
    return render_template('graphs.html', absLnPlt=lstofplots100,div=div,script=script,wvls=wavelength)


if __name__ == '__main__':
    app.debug = True
    app.run()
