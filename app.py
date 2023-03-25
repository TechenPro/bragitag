from flask import Flask, render_template, request
from flask_assets import Environment, Bundle
from bragiengine.bragitag import BragitagEngine

app = Flask(__name__)

engine = BragitagEngine("INSERT CONFIG PATH HERE")
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('styles/index.scss', filters='libsass', output='all.css')
assets.register('scss_all', scss)

js = Bundle('js/main.js', filters='jsmin', output='all.js')
assets.register('js_all', js)

colHeads = ['File Name', 'Path', 'Tag', 'Title', 'Artist', 'Album Artist', 'Album', 'Track', 'Disc Number', 'Year',  'Genre', 'Comment', 'Codec', 'Bitrate', 'Frequency', 'Length', 'Modified']
rows = []

k = 0
for i in range(0, 100):
    newRow = {}
    for colHead in colHeads:
        newRow[colHead] = k
        k+=1
    rows.append(newRow)

@app.route("/")
def hello_world():
    return render_template('index.html', colHeads=colHeads, rows=rows)

@app.route("/send-info", methods = ['GET', 'POST'])
def upload_file():
    return request

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0')
