from flask import Flask, render_template, Markup, request, jsonify, session
from flask_pymongo import PyMongo
from graph import corrAbs, build_graph_mongo, build_heatmap_mongo, wellIds
from bokeh.embed import components
import os
app = Flask(__name__)
app.secret_key = os.urandom(10)
app.config['MONGO_DBNAME'] = 'ncifred'
app.config['MONGO_URI'] = "mongodb+srv://trinhsk:Bon78952%40@ncifrederick-l7ves.mongodb.net/ncifred?retryWrites=true"
mongo = PyMongo(app)

wavelength = list(range(220,810,10))
pltcodes=[fi for fi in mongo.db.list_collection_names()]

unqPltCodes = list(set([plt[:len(plt)-3] for plt in pltcodes]))
unqPltCodes.sort()
pltcodes.sort()

@app.route('/')
def plotgraphs():
     return render_template('graphs.html', wvls=wavelength,pltcodes=pltcodes,unqPltCodes=unqPltCodes)

@app.route('/updateDf/')
def updateDf():
     selected_pltcode = request.args.get('selected_pltcode').strip()
     lstofplots = []
     for wid in wellIds:
         lstofplots.append(Markup(build_graph_mongo(mongo.db,wavelength,selected_pltcode,wid).decode('utf-8')))#.replace('width="51.84pt"','width="100%"').replace('height="51.84pt"','height="100%"')))
     return jsonify(htmlLinePlt=render_template('updateDF.html',lstofplots=lstofplots),pltcode=selected_pltcode)

@app.route('/updateHeatmap/')
def updateHeatmap():
     selected_pltcode = request.args.get('selected_pltcode').strip()
     selected_wavelength = request.args.get('wavelength').strip()
     p = build_heatmap_mongo(mongo.db,selected_wavelength,selected_pltcode)
     script,div = components(p)
     return jsonify(htmlHeatmap=render_template('updateHeatmap.html',script=script,div=div),pltcode=selected_pltcode,selected_wavelength=selected_wavelength)

@app.route('/updateCorrel/')
def updateCorrel():
    selected_pltcode = request.args.get('selected_pltcode2').strip()
    selected_wavelength = int(request.args.get('wavelength2').strip())
    pltcode100 = selected_pltcode + '100'
    pltcode200 = selected_pltcode + '200'
    corrcoeff = corrAbs(mongo.db,pltcode100,pltcode200,selected_wavelength)
    return jsonify(htmlCorr=render_template('updateCorrl.html', corrcoeff=corrcoeff))

if __name__ == '__main__':
    app.debug = True
    app.run()
