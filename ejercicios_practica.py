#!/usr/bin/env python
'''
SQL Introducción [Python]
Ejercicios de práctica
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
Programa creado para poner a prueba los conocimientos
adquiridos durante la clase
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.1"

import sqlite3
from tkinter.tix import COLUMN

import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Crear el motor (engine) de la base de datos
engine = sqlalchemy.create_engine("sqlite:///secundaria.db")
base = declarative_base()


class Tutor(base):
    __tablename__ = "tutor"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __repr__(self):
        return f"Tutor: {self.name}"


class Estudiante(base):
    __tablename__ = "estudiante"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    grade = Column(Integer)
    tutor_id = Column(Integer, ForeignKey("tutor.id"))

    tutor = relationship("Tutor")

    def __repr__(self):
        return f"Estudiante: {self.name}, edad {self.age}, grado {self.grade}, tutor {self.tutor.name}"


def create_schema():
    # Borrar todos las tablas existentes en la base de datos
    # Esta linea puede comentarse sino se eliminar los datos
    base.metadata.drop_all(engine)

    # Crear las tablas
    base.metadata.create_all(engine) 


def insert_tutor(name):
    # Crear la session
        Session = sessionmaker(bind=engine)
        session = Session()

    # Crear un nuevo tutor
        nuevo_tutor = Tutor(name=name)

    # Agregar el nuevo tutor a la DB
        session.add(nuevo_tutor)
        session.commit()    


def insert_estudiante(name, age, grade, tutor_id):
    # Crear la session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Crear un nuevo estudiante
    nuevo_estudiante = Estudiante(name=name, age=age, grade=grade, tutor_id=tutor_id)
   
    # Agregar el nuevo estudiante a la DB
    session.add(nuevo_estudiante)
    session.commit()    


def fill():
    print('Completemos esta tablita!')
    # Llenar la tabla de la secundaria con al munos 2 tutores
    # Cada tutor tiene los campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del tutor (puede ser solo nombre sin apellido)

    # Llenar la tabla de la secundaria con al menos 5 estudiantes
    # Cada estudiante tiene los posibles campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del estudiante (puede ser solo nombre sin apellido)
    # age --> cuantos años tiene el estudiante 
    # grade --> en que año de la secundaria se encuentra (1-6)
    # tutor --> el tutor de ese estudiante (el objeto creado antes)

    # No olvidarse que antes de poder crear un estudiante debe haberse
    # primero creado el tutor. 
    tutores = ["Alejandro","Lorena","Silvia"] 

    for x in range(len(tutores)): 
        insert_tutor(tutores[x]) 


    estudiantes = [("Victoria",17,5,1),
                   ("Alvaro",15,3,2 ) ,
                   ("Laura",16,4,3) ,
                   ("Jorge",13,1,1,) ,   
                   ("Julieta",18,6,2) ]   

    for x in range(len(estudiantes)):
        insert_estudiante(estudiantes[x][0] ,estudiantes[x][1], estudiantes[x][2], estudiantes[x][3])                               
    
                            

def fetch():
    print('Comprovemos su contenido, ¿qué hay en la tabla?')
    # Crear una query para imprimir en pantalla
    # todos los objetos creaods de la tabla estudiante.
    # Imprimir en pantalla cada objeto que traiga la query
    # Realizar un bucle para imprimir de una fila a la vez
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Estudiante)   

    for estudiante in query: 
        print(estudiante) 

def search_by_tutor(tutor):
    print('Operación búsqueda!')
    # Esta función recibe como parámetro el nombre de un posible tutor.
    # Crear una query para imprimir en pantalla
    # aquellos estudiantes que tengan asignado dicho tutor.

    # Para poder realizar esta query debe usar join, ya que
    # deberá crear la query para la tabla estudiante pero
    # buscar por la propiedad de tutor.name 
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(Estudiante).join(Estudiante.tutor).filter(Tutor.name == tutor)
    print("Estudiantes del tutor", tutor) 

    for x in query:
            print(x.name)




def modify(id, name):
    print('Modificando la tabla')
    # Deberá actualizar el tutor de un estudiante, cambiarlo para eso debe
    # 1) buscar con una query el tutor por "tutor.name" usando name
    # pasado como parámetro y obtener el objeto del tutor
    # 2) buscar con una query el estudiante por "estudiante.id" usando
    # el id pasado como parámetro
    # 3) actualizar el objeto de tutor del estudiante con el obtenido
    # en el punto 1 y actualizar la base de datos

    # TIP: En clase se hizo lo mismo para las nacionalidades con
    # en la función update_persona_nationality 

    Session = sessionmaker(bind=engine)
    session = Session() 

    query = session.query(Tutor).filter(Tutor.name == nuevo_tutor)  
    tutor_activo = query.first() 

    query = session.query(Estudiante).filter(Estudiante.id == id)
    estudiante_activo = query.first() 

    estudiante_activo.tutor = tutor_activo  

    session.add(estudiante_activo) 
    session.commit()

    print("Estudiante actualizado Id:", id)
    



def count_grade(grade):
    print('Estudiante por grado')
    # Utilizar la sentencia COUNT para contar cuantos estudiante
    # se encuentran cursando el grado "grade" pasado como parámetro
    # Imprimir en pantalla el resultado

    # TIP: En clase se hizo lo mismo para las nacionalidades con
    # en la función count_persona 

     # Crear la session
    Session = sessionmaker(bind=engine)
    session = Session() 

    resultado = session.query(Estudiante).filter(Estudiante.grade == grade).count()
    print("Estudiantes en grado:", grade, "encontrados:", resultado) 

if __name__ == '__main__':
    print("Bienvenidos a otra clase de Inove con Python")
    create_schema()   # create and reset database (DB)
    fill()
    fetch()

    tutor = 'Andrea'
    search_by_tutor(tutor)

    nuevo_tutor = 'Alberto'
    id = 2
    modify(id, nuevo_tutor)

    grade = 2
    count_grade(grade)  


    


    
           
