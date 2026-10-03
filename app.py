from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Organizador, Evaluador
import os

app=Flask(__name__)
app.secret_key = 'your_secret_key'

app.config.from_pyfile('config.py')

#Configuración para subida de archivos
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


db.init_app(app)

from gestor import GestorDB
gestor = GestorDB()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    return redirect(url_for('login'))


#=======================================================LOGIN===========================================================#

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not request.form['correo'] or not request.form['clave']:
            flash('Por favor, ingrese su correo y contraseña', 'warning')
            return render_template('auth/login.html')

        usuario = gestor.validarLogin(
            request.form['correo'],
            request.form['clave']
        )

        if usuario is None:
            flash('Correo o contraseña incorrectos', 'danger')
            return render_template('auth/login.html')

        tipoUsuario = gestor.getTipoUsuario(usuario)

        session['userId'] = usuario.getId()
        session['tipoUsuario'] = tipoUsuario

        flash(f'Bienvenido/a {usuario.getNombre()}', 'success')

        if tipoUsuario == 'organizador':
            return redirect(url_for('dashboardOrganizador'))

        if tipoUsuario == 'evaluador':
            return redirect(url_for('dashboardEvaluador'))

    return render_template('auth/login.html')




#============================ Rutas Para funcionalidades Autor=========================================================#

@app.route('/enviarTrabajo', methods=['GET', 'POST'])
def enviarTrabajo():
    if request.method == 'POST':
        if not request.form['titulo'] or not request.form['resumen'] or not request.form['area']:
            flash('Por favor complete todos los campos del trabajo', 'warning')
            return render_template('autor/enviarTrabajo.html')
        
        if not request.form['nombre'] or not request.form['apellido'] or not request.form['correo']:
            flash('Por favor complete los datos del autor', 'warning')
            return render_template('autor/enviarTrabajo.html')
        
        archivo = request.files.get('archivo')
        
        if not archivo or archivo.filename == '':
            flash('Debe seleccionar un archivo para el trabajo', 'warning')
            return render_template('autor/enviarTrabajo.html')
        
        trabajo_id = gestor.crearTrabajo(
            request.form['titulo'],
            request.form['resumen'],
            request.form['area'],
            request.form['nombre'],
            request.form['apellido'],
            request.form['correo'],
            archivo
        )
        
        if trabajo_id:
            flash(f'Trabajo registrado correctamente. Número de trabajo: {trabajo_id}', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error al registrar el trabajo', 'danger')
            return render_template('autor/enviarTrabajo.html')
    
    return render_template('autor/enviarTrabajo.html')

 
@app.route('/consultarTrabajo', methods=['GET', 'POST'])
def consultarTrabajo():
        pass


#===========================================================================================================================================#



#=====================================Rutas Para funcionalidades Organizador===========================================================#

@app.route('/organizador/dashboard')
def dashboardOrganizador():
    return render_template('organizador/dashboard.html')
 
@app.route('/organizador/ejecutarAsignacion', methods=['POST'])
def ejecutarAsignacion():
    if session.get('tipoUsuario') != 'organizador':
        flash('Debe ingresar como organizador para ejecutar esta acción', 'danger')
        return redirect(url_for('login'))

    trabajos_incompletos = gestor.ejecutarAsignacion()

    flash('El proceso de asignación ha finalizado', 'success')

    if trabajos_incompletos > 0:
        flash(f'Hay {trabajos_incompletos} trabajo/s que no pudieron completar las 3 asignaciones.', 'warning')

    return redirect(url_for('dashboardOrganizador'))



#===========================================================================================================================================#


#------------------------ Rutas Para funcionalidades Evaluador---------------------------------------------------#

@app.route('/evaluador/dashboard')
def dashboardEvaluador():
    return render_template('evaluador/dashboard.html')

#------------------------------------------------------------------------------------------------------------------#




if __name__ == '__main__':     
    with app.app_context():   
        gestor.crearDB()       
        app.run(debug = True)   

