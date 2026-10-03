from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

db = SQLAlchemy()

class Organizador(db.Model):
    __tablename__ = 'organizadores'
    id = db.Column(db.Integer, primary_key=True)    
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    clave = db.Column(db.String(100), nullable=False)


    def getId(self):
        return self.id

    def getNombre(self):
        return self.nombre

    def getApellido(self):
        return self.apellido

    def getCorreo(self):
        return self.correo

    def getClave(self):
        return self.clave

    def verificaClave(self, clave):
        return check_password_hash(self.clave, clave)
 
 
class Evaluador(db.Model):
    __tablename__ = 'evaluadores'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(5))
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    area = db.Column(db.String(3), nullable=False)    
    max_trabajos = db.Column(db.Integer, nullable=False, default=3)
    clave = db.Column(db.String(100), nullable=False)        
    asignaciones = db.relationship('Asignacion', backref='evaluador', lazy=True)

    def getId(self):
        return self.id
    def getNombre(self):
        return self.nombre
    def getApellido(self):
        return self.apellido
    def getCorreo(self):
        return self.correo
    def getArea(self):
        return self.area
    def getMaxTrabajos(self):
        return self.max_trabajos
    def getClave(self):
        return self.clave
    def getAsignaciones(self):
        return self.asignaciones
    def verificaClave(self, clave):
        return check_password_hash(self.clave, clave)
    
class Trabajo(db.Model):
    __tablename__ = 'trabajos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    resumen = db.Column(db.Text, nullable=False)
    area = db.Column(db.String(3), nullable=False)
    autor_nombre = db.Column(db.String(100), nullable=False)
    autor_apellido = db.Column(db.String(100), nullable=False)
    autor_email = db.Column(db.String(120), nullable=False)
    estado = db.Column(db.String(20), default='Pendiente') 
    fecha_envio = db.Column(db.DateTime, default=datetime.now)
    archivo_nombre = db.Column(db.String(255), nullable=True)        
    asignaciones = db.relationship('Asignacion', backref='trabajo', lazy=True)
    

    def getId(self):
        return self.id

    def getTitulo(self):
        return self.titulo

    def getResumen(self):
        return self.resumen

    def getArea(self):
        return self.area

    def getAutorNombre(self):
        return self.autor_nombre

    def getAutorApellido(self):
        return self.autor_apellido

    def getAutorEmail(self):
        return self.autor_email

    def getEstado(self):
        return self.estado

    def getFechaEnvio(self):
        return self.fecha_envio

    def getArchivoNombre(self):
        return self.archivo_nombre

    def getAsignaciones(self):
        return self.asignaciones



class Asignacion(db.Model):
    __tablename__ = 'asignaciones'
    id = db.Column(db.Integer, primary_key=True)
    trabajo_id = db.Column(db.Integer, db.ForeignKey('trabajos.id'), nullable=False)
    evaluador_id = db.Column(db.Integer, db.ForeignKey('evaluadores.id'), nullable=False)
    valoracion = db.Column(db.Integer, nullable=True) 
    comentarios = db.Column(db.Text, nullable=True)
    fecha_evaluacion = db.Column(db.DateTime, nullable=True)

    def getId(self):
        return self.id

    def getTrabajoId(self):
        return self.trabajo_id

    def getEvaluadorId(self):
        return self.evaluador_id

    def getValoracion(self):
        return self.valoracion

    def getComentarios(self):
        return self.comentarios

    def getFechaEvaluacion(self):
        return self.fecha_evaluacion