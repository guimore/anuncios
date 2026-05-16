from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# CONFIGURACIÓN DE LA BASE DE DATOS
# Esto crea el archivo database_blog.db en tu carpeta
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'database_blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELO DE LA NOTICIA (La estructura de la tabla)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    vistas = db.Column(db.Integer, default=0)

# RUTA 1: EL HOME (Usa tu index.html)
@app.route('/')
def index():
    # Trae todas las noticias de la DB, las más nuevas primero
    noticias = Post.query.order_by(Post.fecha.desc()).all()
    return render_template('index.html', noticias=noticias)

# RUTA 2: EL REDACTOR (Para crear entradas)
@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        
        nueva_noticia = Post(titulo=titulo, contenido=contenido)
        db.session.add(nueva_noticia)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('editor.html')

# INICIALIZADOR DEL SISTEMA
if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Esto crea el archivo .db si no existe
    app.run(debug=True, port=5002)