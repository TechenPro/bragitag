from flask import Flask, render_template, request
from flask_assets import Environment, Bundle
from bragiengine.bragitag import BragitagEngine
import json

app = Flask(__name__)

engine = BragitagEngine("C:\\Users\\mpnef\\Desktop\\HackUSU 2023\\bragiengine\\.config")
dir_tree = engine.load_dir_tree()
dir_tree_json = json.dumps(dir_tree)
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('styles/index.scss', filters='libsass', output='all.css')
assets.register('scss_all', scss)

js = Bundle('js/main.js', filters='jsmin', output='all.js')
assets.register('js_all', js)

colHeads = ['File Name', 'Path', 'Tag', 'Title', 'Artist', 'Album Artist', 'Album', 'Track', 'Disc Number', 'Year',  'Genre', 'Comment', 'Codec', 'Bitrate', 'Frequency', 'Length', 'Modified']
rows = []

k = 0
for i in range(0, 30):
    newRow = {}
    for colHead in colHeads:
        newRow[colHead] = k
        k+=1
    rows.append(newRow)

@app.route("/")
def hello_world():
    return render_template('index.html', colHeads=colHeads, rows=rows, dir_tree=dir_tree, dir_tree_json=dir_tree_json)

@app.route("/send-info", methods = ['POST'])
def upload_file():
    if request.method == 'POST':
      f = request.files['file']
      print(type(f))
    #   f.save(secure_filename(f.filename))
      return 'file uploaded successfully'
    
@app.route("/change-dir", methods = ['POST'])
def change_dir():
    if request.method == 'POST':
      # ayo
      return 'THIS SHOULD BE THE LOADED DATA'

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0')
