from flask import Flask, render_template, request
from flask_assets import Environment, Bundle
from bragiengine.bragitag import BragitagEngine
import json

app = Flask(__name__)

engine = BragitagEngine("/app/.config")
dir_tree = engine.get_dir_tree()
dir_tree_json = json.dumps(dir_tree)
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('styles/index.scss', filters='libsass', output='all.css')
assets.register('scss_all', scss)

js = Bundle('js/main.js', filters='jsmin', output='all.js')
assets.register('js_all', js)

colHeads = ['File Name', 'Parent Dir', 'Title', 'Artist', 'Album Artist', 'Composer', 'Album',
            'Track', 'Disc Number', 'Year',  'Genre', 'Comment', 'Codec', 'Bitrate', 'Frequency', 'Length']
colHeadsJSON = json.dumps(colHeads)
rows = []

for i in range(0, 30):
    newRow = {}
    for colHead in colHeads:
        newRow[colHead] = ""
    rows.append(newRow)


@app.route("/")
def hello_world():
    return render_template('index.html', colHeads=colHeads, colHeadsJSON=colHeadsJSON, rows=rows, dir_tree=dir_tree, dir_tree_json=dir_tree_json)


@app.route("/send-info", methods=['POST'])
def upload_file():
    if request.method == 'POST':
        data = json.loads(request.form["json"])
        if "file" in data:
            f = request.files['file']
            data["changes"]["artwork"] = f
        result = engine.edit_file_metadata(data)

        return "done"


@app.route("/change-dir", methods=['POST'])
def change_dir():
    if request.method == 'POST':
        subdir = request.data.decode()
        data = engine.change_active_dir(engine.root_dir + "/" + subdir)
        return data


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
