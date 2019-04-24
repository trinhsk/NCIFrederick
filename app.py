from flask import Flask, render_template
from graph import build_graph, pd
 
app = Flask(__name__)

dfm100 = pd.read_csv('/users/trinhsk/Documents/absVizFlask/textfiles/14190301100.txt',encoding='utf-16',sep='\t',skiprows=2,skipfooter=2,engine='python')

dfm200 = pd.read_csv('/users/trinhsk/Documents/absVizFlask/textfiles/14190301200.txt',encoding='utf-16',sep='\t',skiprows=2,skipfooter=2,engine='python')

@app.route('/graphs')
def graphs():
     
    graph_url = build_graph(dfm);
 
    return render_template('graphs.html', absLnPlt=graph_url)
 
if __name__ == '__main__':
    app.debug = True
    app.run()
