from flask import Flask, render_template, request, send_from_directory, Blueprint, current_app, redirect, url_for
import os
from werkzeug.utils import secure_filename

bp = Blueprint('explore', __name__, url_prefix='/explore')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def get_absolute_path(relative_path):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    full_path = os.path.join(upload_folder, relative_path)
    if not os.path.abspath(full_path).startswith(os.path.abspath(upload_folder)):
        return None
    return full_path

@bp.route('/', defaults={'subpath': ''})
@bp.route('/<path:subpath>')
def index(subpath):
    abs_path = get_absolute_path(subpath)
    if not abs_path or not os.path.exists(abs_path):
        return "Path not found", 404
    
    if os.path.isfile(abs_path):
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], subpath)
    
    files = []
    dirs = []
    for item in os.listdir(abs_path):
        item_path = os.path.join(abs_path, item)
        if os.path.isdir(item_path):
            dirs.append((item, os.path.join(subpath, item)))
        else:
            files.append((item, os.path.join(subpath, item)))
    
    return render_template('index.html', dirs=dirs, files=files, current_path=subpath)

@bp.route('/upload', methods=['POST'])
def upload_file():
    subpath = request.form.get('current_path', '')
    abs_path = get_absolute_path(subpath)
    
    if 'file' not in request.files or not abs_path:
        return 'Invalid request'
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(abs_path, filename))
        return redirect(url_for('explore.index', subpath=subpath))
    
    return 'Invalid file type'

@bp.route('/mkdir', methods=['POST'])
def mkdir():
    subpath = request.form.get('current_path', '')
    dirname = secure_filename(request.form.get('dirname', ''))
    if not dirname:
        return 'Invalid folder name'
    
    abs_path = get_absolute_path(subpath)
    new_dir = os.path.join(abs_path, dirname)
    
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    
    return redirect(url_for('explore.index', subpath=subpath))

@bp.route('/rename', methods=['POST'])
def rename():
    subpath = request.form.get('current_path', '')
    old_name = secure_filename(request.form.get('old_name'))
    new_name = secure_filename(request.form.get('new_name'))
    
    if not old_name or not new_name:
        return 'Invalid names'
    
    abs_path = get_absolute_path(subpath)
    old_path = os.path.join(abs_path, old_name)
    new_path = os.path.join(abs_path, new_name)
    
    if os.path.exists(old_path) and not os.path.exists(new_path):
        os.rename(old_path, new_path)
    
    return redirect(url_for('explore.index', subpath=subpath))