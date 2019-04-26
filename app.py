from flask import Flask, render_template, Markup, request, jsonify
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
        return render_template('graphs.html', absLnPlt=lstofplots100, wvls=wavelength)

@app.route('/updateHeatmap/')
def updateHeatmap():
     pltcode='14190302100'
     selected_wavelength = request.args.get('wavelength')
     print(selected_wavelength)
     row = wavelength.index(int(selected_wavelength))
     p = build_heatmap(dfm100,row,selected_wavelength,pltcode)
     script,div = components(p) 
     return jsonify(htmlHeatmap=render_template('updateHeatmap.html',script=script,div=div),pltcode=pltcode,selected_wavelength=selected_wavelength)

if __name__ == '__main__':
    app.debug = True
    app.run()
