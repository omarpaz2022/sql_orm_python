# Ejercicios de práctica [Python]
#A esta altura del curso el alumno posee ya una serie de habilidades muy vinculadas entre si las cuales son:
#- Análisis, filtrado y trabajo de información.
#- Capacidad para utilizar formatos de datos de transacciones, APIs, Apps.
#- Manipular y crear base de datos.

#EL propósito de este ejercicio es que el alumno ponga a prueba estas facultades con un clásico ejercicio de 
#"challenge" técnico de Mercado Libre (MELI), lo próximo que se verá de aquí en más son herramientas o procesos para mejorar estos 3 pilares (bases de datos, JSON, consumir API).

# MELI API [Python]
#Haremos uso de la API pública de mercadolibre para obtener los datos de items a la venta, muy similar a lo que ya 
#estuvieron practicando pero dándole el enfoque de una problemática real.

# Enunciado
#El objetivo es consumir los datos que provee el archivo CSV "meli_technical_challenge_data.csv". Dicho archivo 
#está compuesto por la siguiente estructura:
#- Columna site --> columna texto de 3 caracteres
#- Coulmna id --> columna numérica

#Nota: Alumno debe descartar aquellas filas que presente datos corruptos o incompletos.\
#Con el site + id se forma el "id" del producto (item), por ejemplo la primera file tiene:
#- site: MLA
#- id: 845041373

#Esto forma el item con id MLA845041373\

#El objetivo es que utilicen la siguiente API URL para consumir la información de cada item en la lista:
#url = 'https://api.mercadolibre.com/items?ids=MLA845041373'

#Debe reemplazar en el string de la URL con cada item id que formen a partir del archivo CSV. Cada consulta 
#les traerá la siguiente información (ejemplo con MLA845041373):

#```
#{
 # "code": 200,
  #"body": [
   # "id": "MLA845041373",
    #"site_id": "ML4",
    #"title": "Medidor Digital De Energía, Voltaje 100a,",
    #...
    #"price": 2900,
    #...
    #"currency_id": "ARS"
    #...
    #"initial_quantity": 4,
    #"available_quantity": 0,
    #"sold_quantity": 4,
    #...
#}
#```

#Nota: Alumno solo es necesario que capture todos los campos especificados en el ejemplo anterior, si alguno 
#de los campos no está disponible en la consulta debe descartar ese item. Los campos en definitiva importantes son:
#- id
#- site_id
#- title
#- price
#- currency_id
#- initial_quantity
#- available_quantity
#- sold_quantity

#Notar que en el medio de la URL se está especificando que queremos obtener los Departamentos y Alquileres 
#en la Ciudad de "__Mendoza__". Esto pueden modificarlo para jugar y obtener diferentes resultados.


## create_schema
#Deben crear una función "create_schema" la cual se encargará de crear la base de datos y la tabla correspondiente 
#al esquema definido. Deben usar la sentencia CREATE para crear la tabla con los campos mencionados.\
#IMPORTANTE: Recuerden que es recomendable borrar la tabla (DROP) antes de crearla si es que existe para que 
#no haya problemas al ejecutar la query.

## fill()
#Deben crear una función "fill" que lea los datos del archivo CSV y cargue las respuestas de la API como filas 
#de la tabla SQL. Pueden resolverlo de la forma que mejor crean. Deben usar la sentencia INSERT para insertar los datos.\

## fetch(id)
#Deben crear una función que imprima en pantalla filas de su base de datos, pueden usar esta función para ver 
#que "fill" realizó exactamente lo que era esperado. Deben usar la sentencia SELECT para llegar al objetivo junto
# con WHERE para leer la fila deseada (si se desea leer una en particular).\
#Esta función recibe como parámetro un id (ejemplo MLA845041373) deben imprimir sola la fila correspondiente a ese id.
#IMPORTANTE: Es posible que pasen como id un item no definido en la tabla y el sistema de fetchone les devuelva None
# lo cual es correcto, pero el sistema no debe explotar porque haya retornado None. En ese caso pueden imprimir 
#en pantalla que no existe esa fila en la base de datos (más adelante en una API responderá Error 404).

#```
#if __name__ == "__main__":
  # Crear DB
  #create_schema()

  # Completar la DB con el CSV
  #fill()

  # Leer filas
  #fetch('MLA845041373')
  #fetch('MLA717159516')

#```

## Para jugar
#Cuando finalicen el ejercicio pueden realizar un sistema de compras. Pueden pasarle a su sistema el carrito 
#de un cliente con todos los IDs de los productos comprados por la persona y el sistema podría devolver el monto total de compra.

## Anexo
#En la carpeta de anexo encontrará este ejercicio resuelto, como también una forma mejorada utilizando "async"
# para acelerar drástica mente el código (async no fue visto en clase y requeire instalar una librería adicional 
#como se explica en el ejercicio).

import json
import requests
import sqlite3
import csv
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Crear el motor (engine) de la base de datos llamada "sqlite:///   .db"
engine = sqlalchemy.create_engine("sqlite:///base_dato_productos_mla.db")
base = declarative_base()


class Productos(base):
    __tablename__ = "tablaproductos"
    id = Column(Integer, primary_key=True)
    item_id = Column(String)
    site_id = Column(String)
    title = Column(String)
    price = Column(Integer)
    currency_id = Column(String)
    initial_quantity = Column(Integer)
    available_quantity = Column(Integer)
    sold_quantity = Column(Integer)
   
    def __repr__(self):
        return f"item_id {self.item_id}, site_id {self.site_id}, title {self.title}, price {self.price}, currency_id {self.currency_id}, initial_quantity {self.initial_quantity}, available_quantity {self.available_quantity}, sold_quantity {self.sold_quantity}"




def create_schema():
    # Borrar todas las tablas existentes en la BD
    base.metadata.drop_all(engine)
    # Crear nuevamente todas las tablas
    base.metadata.create_all(engine)


def insert_producto(item_id, site_id, title, price, currency_id, initial_quantity, available_quantity, sold_quantity):
    # Crear la session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Crear un nuevo producto
    nuevo_producto = Productos(item_id=item_id, site_id=site_id, title=title, price=price, currency_id=currency_id, initial_quantity=initial_quantity, available_quantity=available_quantity, sold_quantity=sold_quantity)
   
    # Agregar el nuevo producto a la DB
    session.add(nuevo_producto)
    session.commit()
    

def fill():
    # Leer el archivo .CSV que contiene las columnas site e id de los productos
    archivo= "meli_technical_challenge_data.csv"
    with open(archivo) as csvfile:
        data = list(csv.DictReader(csvfile))         

    # item_id= site + id
    item_id = [(row["site"] + row["id"]) for row in data]
       
    url = "https://api.mercadolibre.com/items?ids="
 
    for x in range(len(item_id)): 
        response = requests.get(url + item_id[x])
        data = response.json()

        # filtro los datos vacios "None" y guardo los demas en la tabla "tablaproductos" dentro de la DB "base_dato_productos_mla.db"
        if data[0]["body"].get("id") != None and data[0]["body"].get("site_id") != None and data[0]["body"].get("title") != None and data[0]["body"].get("price") != None and data[0]["body"].get("currency_id") != None and data[0]["body"].get("initial_quantity") != None and data[0]["body"].get("available_quantity") != None and data[0]["body"].get("sold_quantity") != None:
            insert_producto(data[0]["body"].get("id"), data[0]["body"].get("site_id"), data[0]["body"].get("title"), data[0]["body"].get("price"), data[0]["body"].get("currency_id"), data[0]["body"].get("initial_quantity"), data[0]["body"].get("available_quantity"), data[0]["body"].get("sold_quantity"))
    return 


def fetch(item_id): 
    # Crear la session
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(Productos).filter(Productos.item_id == item_id)
    search = query.first()

    if search != None :
        print(search)
    else:
        print("Producto no encontrado")
    return


if __name__ == '__main__':
    
    # reset and create database (DB)
    create_schema()   

    fill()
    
    # Leer filas segun item_id
    fetch("MLA845041373")
    fetch("MLA717159516")