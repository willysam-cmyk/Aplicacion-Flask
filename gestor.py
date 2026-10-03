from datetime import datetime
from werkzeug.security import generate_password_hash
from models import db, Organizador, Evaluador, Trabajo, Asignacion
import os
from werkzeug.utils import secure_filename
from flask import current_app

class GestorDB:
    def crearDB(self):
        db.create_all()

    def crear_organizador(self, nombre, apellido, correo):
        organizador = Organizador(nombre=nombre,apellido=apellido,correo=correo,clave=generate_password_hash("admin"))
        if not organizador.id():
            db.session.add(organizador)
            db.session.commit()

    
    def crear_evaluador(self, titulo, nombre, apellido, correo, area, max_trabajos):
        evaluador = Evaluador(titulo=titulo, nombre=nombre, apellido=apellido, correo=correo, area=area, max_trabajos=max_trabajos, clave=generate_password_hash("123"))
        if not evaluador.id():
            db.session.add(evaluador)
            db.session.commit()

    def getOrganizadorPorCorreo(self, correo):
        return Organizador.query.filter_by(correo=correo).first()

    def getEvaluadorPorCorreo(self, correo):
        return Evaluador.query.filter_by(correo=correo).first()

    def validarLogin(self, correo, clave):
        usuario = None

        organizador = self.getOrganizadorPorCorreo(correo)

        if organizador is not None and organizador.verificaClave(clave):
            usuario = organizador
        else:
            evaluador = self.getEvaluadorPorCorreo(correo)

            if evaluador is not None and evaluador.verificaClave(clave):
                usuario = evaluador

        return usuario


    def getTipoUsuario(self, usuario):
        valor=None
        if isinstance(usuario, Organizador):
            valor = 'organizador'
        elif isinstance(usuario, Evaluador):
            valor = 'evaluador'

        return valor    
        
    
    def crearTrabajo(self, titulo, resumen, area, autor_nombre, autor_apellido, autor_email, archivo):
        
        filename = secure_filename(archivo.filename)
        nombre_archivo = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        archivo.save(os.path.join(current_app.config['UPLOAD_FOLDER'], nombre_archivo))
        
        nuevoTrabajo = Trabajo(
            titulo=titulo,
            resumen=resumen,
            area=area,
            autor_nombre=autor_nombre,
            autor_apellido=autor_apellido,
            autor_email=autor_email,
            estado='Pendiente',
            fecha_envio=datetime.now(),
            archivo_nombre=nombre_archivo  
        )
        
        if not nuevoTrabajo.id:
            db.session.add(nuevoTrabajo)
            db.session.commit()
            return nuevoTrabajo.id
        return None



    def getAsignacionesPorTrabajo(self, trabajo_id):
        return Asignacion.query.filter_by(trabajo_id=trabajo_id).all()
       

    def getTrabajosPendientes(self):
        return Trabajo.query.filter_by(estado='Pendiente').all()


    def getEvaluadoresPorArea(self, area):
        return Evaluador.query.filter_by(area=area).all()

    def crearAsignacion(self, trabajo_id, evaluador_id):
        nuevaAsignacion = Asignacion(trabajo_id=trabajo_id,evaluador_id=evaluador_id)

        if not nuevaAsignacion.id:
            db.session.add(nuevaAsignacion)
            db.session.commit()


    def buscarAsignacionTrabajo(self, asignaciones, trabajo_id):
        i = 0

        while i < len(asignaciones) and asignaciones[i].getTrabajoId() != trabajo_id:
            i += 1

        if i < len(asignaciones):
            retorno = i
        else:
            retorno = -1

        return retorno

    def ejecutarAsignacion(self):
        trabajos = self.getTrabajosPendientes()
        trabajos_incompletos = 0

        for trabajo in trabajos:
            cantidad_asignaciones = len(trabajo.getAsignaciones())

            if cantidad_asignaciones < 3:
                evaluadores = self.getEvaluadoresPorArea(trabajo.getArea())

                for evaluador in evaluadores:
                    if cantidad_asignaciones < 3:
                        asignaciones_evaluador = evaluador.getAsignaciones()

                        posicion = self.buscarAsignacionTrabajo(
                            asignaciones_evaluador,
                            trabajo.getId()
                        )

                        cantidad_trabajos_evaluador = len(asignaciones_evaluador)

                        if posicion == -1 and cantidad_trabajos_evaluador < evaluador.getMaxTrabajos():
                            self.crearAsignacion(trabajo.getId(),evaluador.getId())
                            cantidad_asignaciones += 1

            if cantidad_asignaciones < 3:
                trabajos_incompletos += 1

        return trabajos_incompletos


 