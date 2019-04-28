from flask import Flask, render_template, Markup, request, jsonify, session
# from flask_pymongo import PyMongo
from graph import build_graph, build_heatmap, pd, stripDF, corrAbs
from bokeh.embed import components
import os

app = Flask(__name__)
app.secret_key = os.urandom(10)
# app.config['MONGO_DBNAME'] = 'NCIFredFlaskApp'
# app.config['MONGO_URI'] = 'mongodb+srv://sktrinh12:bon78952@ncifredflaskapps-nr4nv.mongodb.net/test?retryWrites=true'
# mongo = PyMongo(app)

textfile_filepath = app.root_path+'/textfiles/'
wavelength = list(range(220,810,10))
pltcodes=[]
for file in os.listdir(textfile_filepath):
    if file.endswith(".txt"):
        pltcodes.append(file.replace('.txt',''))
unqPltCodes = list(set([plt[:len(plt)-3] for plt in pltcodes]))

@app.route('/')
def plotgraphs():
     return render_template('graphs.html', wvls=wavelength,pltcodes=pltcodes,unqPltCodes=unqPltCodes)

@app.route('/updateDf/')
def updateDf():
     selected_pltcode = request.args.get('selected_pltcode')
     dfm = pd.read_csv(app.root_path + "/textfiles/" + selected_pltcode.strip() + ".txt",encoding='utf-16',sep='\t',skiprows=2,skipfooter=2,engine='python')
     dfm = stripDF(dfm)
     lstofplots = []
     for i in range(384):
         lstofplots.append(Markup(build_graph(dfm,wavelength,i).decode('utf-8')))
     return jsonify(htmlLinePlt=render_template('updateDF.html',lstofplots=lstofplots),pltcode=selected_pltcode)

@app.route('/updateHeatmap/')
def updateHeatmap():
     selected_pltcode = request.args.get('selected_pltcode')
     selected_wavelength = request.args.get('wavelength')
     row = wavelength.index(int(selected_wavelength))
     dfm = pd.read_csv(app.root_path + "/textfiles/" + selected_pltcode.strip() + ".txt",encoding='utf-16',sep='\t',skiprows=2,skipfooter=2,engine='python')
     dfm = stripDF(dfm)
     p = build_heatmap(dfm,row,selected_wavelength,selected_pltcode)
     script,div = components(p)
     return jsonify(htmlHeatmap=render_template('updateHeatmap.html',script=script,div=div),pltcode=selected_pltcode,selected_wavelength=selected_wavelength)

@app.route('/updateCorrel/')
def updateCorrel():
    selected_pltcode = request.args.get('selected_pltcode2')
    selected_wavelength = request.args.get('wavelength2')
    row = wavelength.index(int(selected_wavelength))
    dfm1 = pd.read_csv(app.root_path + "/textfiles/" + selected_pltcode.strip() + "100" +  ".txt",encoding='utf-16',sep='\t',skiprows=2,skipfooter=2,engine='python')
    dfm2 = pd.read_csv(app.root_path + "/textfiles/" + selected_pltcode.strip() + "200" + ".txt",encoding='utf-16',sep='\t',skiprows=2,skipfooter=2,engine='python')
    dfm1 = stripDF(dfm1)
    dfm2 = stripDF(dfm2)
    corrcoeff = corrAbs(dfm1,dfm2,row)
    return jsonify(htmlCorr=render_template('updateCorrl.html', corrcoeff=corrcoeff))

if __name__ == '__main__':
    app.debug = True
    app.run()
