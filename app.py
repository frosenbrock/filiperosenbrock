import json
import os
from flask import Flask, render_template, send_from_directory, request, redirect, url_for

# --- Configuration ---
app = Flask(__name__, static_url_path='/static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000

# --- System & SEO Routes ---

@app.route('/health')
def health_check():
    return {"status": "healthy", "version": "1.1.0"}, 200

@app.route('/robots.txt')
@app.route('/sitemap.xml')
@app.route('/favicon.ico')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/.well-known/security.txt')
@app.route('/security.txt')
def security_txt():
    return send_from_directory(app.static_folder, 'security.txt')

# --- Helper Functions ---

def load_data(file_name):
    file_path = os.path.join(app.root_path, 'data', file_name)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {file_name.replace('.json', ''): []}

# --- Main Routes ---

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/calculocorreto/')
@app.route('/calculo-correto')
@app.route('/calculo-correto/')
@app.route('/calculocorreto')
def calculocorreto():
    if not request.path.endswith('/'):
        return redirect('/calculocorreto/', code=301)
    
    data = load_data('calculo.json')
    return render_template('calculo_correto.html', 
                           title="Cálculo Correto", 
                           tools=data.get('calculo', []))

@app.route('/toolverse/')
@app.route('/toolverse')
def toolverse():
    if request.path == '/toolverse':
        return redirect('/toolverse/', code=301)
        
    data = load_data('toolverse.json')
    return render_template('toolverse.html', 
                           title="Toolverse", 
                           description="Global developer utilities and web tools.",
                           tools=data.get('toolverse', []))

# --- Security Headers & Error Handling ---

@app.after_request
def add_header(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', 
                           error_code=404, 
                           message="Oops! Page not found."), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', 
                           error_code=500, 
                           message="Something went wrong on our end."), 500

if __name__ == '__main__':
    app.run(debug=True)