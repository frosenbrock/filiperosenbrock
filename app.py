import json
import os
from flask import Flask, render_template, send_from_directory, request, redirect, url_for

app = Flask(__name__)

@app.route('/robots.txt')
@app.route('/sitemap.xml')
@app.route('/favicon.ico')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

def load_data(file_name):
    file_path = os.path.join(app.root_path, 'data', file_name)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {file_name.replace('.json', ''): []}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/calculocorreto/')
def calculocorreto():
    data = load_data('calculo.json')
    return render_template('calculo_correto.html', 
                           title="Cálculo Correto", 
                           description="Brazilian labor and financial calculators.",
                           tools=data.get('calculo', []))

@app.route('/calculo-correto')
@app.route('/calculo-correto/')
def old_calculo_correto_redirect():
    return redirect(url_for('calculocorreto'), code=301)

@app.route('/calculocorreto')
def clean_calculocorreto_url():
    return redirect(url_for('calculocorreto'), code=301)

@app.route('/toolverse/')
def toolverse():
    data = load_data('toolverse.json')
    return render_template('toolverse.html', 
                           title="Toolverse", 
                           description="Global developer utilities and web tools.",
                           tools=data.get('toolverse', []))

@app.route('/toolverse')
def clean_toolverse_url():
    return redirect(url_for('toolverse'), code=301)

if __name__ == '__main__':
    app.run(debug=True)