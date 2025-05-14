from flask import Flask, render_template, request, send_from_directory, g, redirect, url_for
import os



def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'uploads'

    app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    import explore
    app.register_blueprint(explore.bp)


    @app.route('/')
    def index():
        return redirect(url_for('explore.index'))

    @app.before_request
    def set_g():
        g.user = lambda x:...
        g.user.config={}
        g.user.config['id'] = 1


    return app



# def create_app():
#     app = Flask(__name__)
#     app.config['UPLOAD_FOLDER'] = 'uploads'
#     app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    
#     # Создать папку uploads если не существует
#     if not os.path.exists(app.config['UPLOAD_FOLDER']):
#         os.makedirs(app.config['UPLOAD_FOLDER'])
    
#     import explore
#     app.register_blueprint(explore.bp)
    
#     return app